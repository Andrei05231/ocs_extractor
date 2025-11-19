from config.db_config import DBConfig
from core.db import OCSDatabase
from exporter.csv_exporter import CSVExporter
from layouts.default_layout import apply_layout

def main():
    db_config = DBConfig()
    db = OCSDatabase(db_config)

    try:
        db.connect()
        df = db.fetch_hardware(['cpu','gpu','memory','user','monitor'])

        df = apply_layout(df,{'format_memory': True, 'reverse_gpus': True})

        exporter = CSVExporter()
        exporter.export(df, "ocs_custom_invetory.csv")

    finally:
        db.close()


if __name__ == "__main__":
    main()
