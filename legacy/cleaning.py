import sqlite3


# Step 1: Define the Strategy Interface
class DatabaseMigrationStrategy:
    def migrate(self, cur):
        pass


# Step 2: Implement Concrete Strategies
class DateColumnMigration(DatabaseMigrationStrategy):
    def migrate(self, cur):
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     ADD COLUMN data_situacao_especial_1 DATE")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     ADD COLUMN data_situacao_especial_2 TEXT")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                    data_situacao_especial_2 = data_situacao_especial")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     data_situacao_especial_2 = substr(\
                    data_situacao_especial_2, 0, 5) || '-' ||\
                     substr(data_situacao_especial_2, 5, 2) ||\
                     '-' || substr(data_situacao_especial_2, 7, 2)")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     data_situacao_especial_1 = data_situacao_especial_2")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     DROP COLUMN data_situacao_especial_2")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     DROP COLUMN data_situacao_especial")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     RENAME COLUMN data_situacao_especial_1 TO\
                     data_situacao_especial")
        cur.execute("COMMIT")


class CnpjColumnMigration(DatabaseMigrationStrategy):
    def migrate(self, cur):
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     ADD COLUMN cnpj_completo TEXT")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     cnpj_completo = '0' || cnpj_basico_id || '/000' ||\
                     matriz_filial || '-' || cnpj_dv WHERE\
                     length(cnpj_basico_id) = 7")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     cnpj_completo = cnpj_basico_id || '/000' ||\
                     matriz_filial || '-' || cnpj_dv WHERE length(\
                    cnpj_basico_id) = 8")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     correio_eletronico = lower(correio_eletronico)")
        cur.execute("COMMIT")


class CepColumnMigration(DatabaseMigrationStrategy):
    def migrate(self, cur):
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     ADD COLUMN cep_1 INTEGER")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     ADD COLUMN cep_2 TEXT")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     cep_1 = cast(substr(cep, 0, 9) as integer)")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     cep_2 = cep_1")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     DROP COLUMN cep_1")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     DROP COLUMN cep")
        cur.execute("ALTER TABLE cnpj_estabelecimentos\
                     RENAME COLUMN cep_2 TO cep")
        cur.execute("UPDATE cnpj_estabelecimentos SET\
                     cep = '0' || cep WHERE length(cep) = 7")
        cur.execute("COMMIT")


# Step 3: Create Context Class
class DatabaseMigrator:
    def __init__(self, migration_strategy):
        self.migration_strategy = migration_strategy

    def setMigrationStrategy(self, migration_strategy):
        self.migration_strategy = migration_strategy

    def executeMigration(self, cur):
        self.migration_strategy.migrate(cur)


# Step 4: Client Code
if __name__ == "__main__":
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    # Create instances of strategies
    date_migration_strategy = DateColumnMigration()
    cnpj_migration_strategy = CnpjColumnMigration()
    cep_migration_strategy = CepColumnMigration()

    # Create a DatabaseMigrator instance with the initial strategy
    migrator = DatabaseMigrator(date_migration_strategy)

    # Execute the initial strategy
    migrator.executeMigration(cur)

    # Switch to a different strategy
    migrator.setMigrationStrategy(cnpj_migration_strategy)
    migrator.executeMigration(cur)

    # Switch to another strategy
    migrator.setMigrationStrategy(cep_migration_strategy)
    migrator.executeMigration(cur)

    # Show how many rows there are in the table cnpj_estabelecimentos
    cur.execute("SELECT COUNT(*) FROM cnpj_estabelecimentos")
    print(cur.fetchall())

    # Close the connection
    conn.close()
