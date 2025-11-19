import pymysql
import pandas as pd
from config.db_config import DBConfig

class OCSDatabase:
    def __init__(self, config: DBConfig):
        self.config = config
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = pymysql.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database
            )

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def fetch_hardware(self, components = None) -> pd.DataFrame:
        """
        Fetch hardware data with optional components.
        components: list of ['cpu', 'gpu', 'memory', 'user'] to include.
        If None, includes all.
        """
        if components is None:
            components = ['cpu', 'gpu', 'memory', 'user']

        # Base select columns and join (BIOS is always included)
        select_cols = [
            "h.NAME AS hardware_name",
            "b.SMODEL AS model_name",
            "b.SSN AS serial_number",
            "h.IPADDR AS ip"
        ]
        joins = ["LEFT JOIN bios b ON b.HARDWARE_ID = h.ID"]

        # Mapping component -> select and join SQL
        component_map = {
            "cpu": (
                "cpu.cpu_type",
                """
                LEFT JOIN (
                    SELECT HARDWARE_ID, GROUP_CONCAT(TYPE ORDER BY ID SEPARATOR ', ') AS cpu_type
                    FROM cpus
                    GROUP BY HARDWARE_ID
                ) cpu ON cpu.HARDWARE_ID = h.ID
                """
            ),
            "gpu": (
                "gpu.gpus",
                """
                LEFT JOIN (
                    SELECT HARDWARE_ID, GROUP_CONCAT(NAME ORDER BY ID SEPARATOR ', ') AS gpus
                    FROM videos
                    GROUP BY HARDWARE_ID
                ) gpu ON gpu.HARDWARE_ID = h.ID
                """
            ),
            "memory": (
                "mem.memory_modules",
                """
                LEFT JOIN (
                    SELECT HARDWARE_ID, GROUP_CONCAT(COALESCE(CAPACITY,0) ORDER BY ID SEPARATOR ' ') AS memory_modules
                    FROM memories
                    GROUP BY HARDWARE_ID
                ) mem ON mem.HARDWARE_ID = h.ID
                """
            ),
            "user": (
                "lu.user_id AS connected_user",
                "LEFT JOIN last_user lu ON lu.hardware_id = h.ID"
            ),
            "monitor": (
                "mon.monitor_serials, mon.monitor_captions",
                """
                LEFT JOIN (
                    SELECT 
                        HARDWARE_ID,
                        GROUP_CONCAT(SERIAL ORDER BY ID SEPARATOR ', ') AS monitor_serials,
                        GROUP_CONCAT(CAPTION ORDER BY ID SEPARATOR ', ') AS monitor_captions
                    FROM monitors
                    GROUP BY HARDWARE_ID
                ) mon ON mon.HARDWARE_ID = h.ID
                """
            )
        }

        # Add optional components
        for comp in components:
            col, join_sql = component_map.get(comp, (None, None))
            if col:
                select_cols.append(col)
                joins.append(join_sql)

        # Build query
        query = f"""
            SELECT {', '.join(select_cols)}
            FROM hardware h
            {' '.join(joins)}
            WHERE h.NAME REGEXP '^[Aa][Rr][Tt][0-9]{{3}}$'
            ORDER BY h.NAME;
        """

        return pd.read_sql(query, self.conn)
