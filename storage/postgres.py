import psycopg2

class PostgresRepository:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        self.connection = psycopg2.connect(self.dsn)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                name TEXT,
                price NUMERIC,
                currency VARCHAR(10),
                brand TEXT,
                sku TEXT,
                availability BOOLEAN
            )
        """)
        self.connection.commit()

    def upsert_product(self, item: dict) -> None:
        self.cursor.execute("""
            INSERT INTO products (url, name, price, currency, brand, sku, availability)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                price = EXCLUDED.price,
                availability = EXCLUDED.availability,
                name = EXCLUDED.name
        """, (
            item.get('url'),
            item.get('name'),
            item.get('price'),
            item.get('currency'),
            item.get('brand'),
            item.get('sku'),
            item.get('availability', True)
        ))
        self.connection.commit()

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()