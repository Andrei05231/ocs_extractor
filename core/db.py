import pymysql
import pandas as pd
from config.db_config import DBConfig

class OCSDatabase:
    def __init__(self, config:DBConfig):
        self.config = config
        self.conn = None


    def connect(self):
        self.conn = pymysql.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database
            )

    def close(self):
        if self.conn:
            self.conn.close()

    def fetch_hardware_with_gpus(self) -> pd.DataFrame:
        query = """
            SELECT 
                h.NAME AS hardware_name,
                    h.USERID AS connected_user,
                        b.SMODEL AS model_name,
                            cpu.cpu_type,
                                h.DESCRIPTION AS device_name,
                                    gpu.gpus,
                                        h.IPADDR AS ip,
                                            mem.memory_modules
                                            FROM hardware h
                                            LEFT JOIN bios b ON b.HARDWARE_ID = h.ID
                                            LEFT JOIN (
                                                        SELECT HARDWARE_ID, GROUP_CONCAT(TYPE ORDER BY ID SEPARATOR ', ') AS cpu_type
                                                            FROM cpus
                                                                GROUP BY HARDWARE_ID
                                                                ) cpu ON cpu.HARDWARE_ID = h.ID
                                            LEFT JOIN (
                                                        SELECT HARDWARE_ID, GROUP_CONCAT(NAME ORDER BY ID SEPARATOR ', ') AS gpus
                                                            FROM videos
                                                                GROUP BY HARDWARE_ID
                                                                ) gpu ON gpu.HARDWARE_ID = h.ID
                                            LEFT JOIN (
                                                        SELECT HARDWARE_ID, GROUP_CONCAT(COALESCE(CAPACITY,0) ORDER BY ID SEPARATOR ' ') AS memory_modules
                                                            FROM memories
                                                                GROUP BY HARDWARE_ID
                                                                ) mem ON mem.HARDWARE_ID = h.ID
                                            WHERE h.NAME REGEXP '^[Aa][Rr][Tt][0-9]{3}$'
                                            ORDER BY h.NAME;
                                            """
        return pd.read_sql(query, self.conn)
