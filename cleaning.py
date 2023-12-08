import sqlite3

conn = sqlite3.connect('db.sqlite3')

cur = conn.cursor()

"""
# Create a new column data_situacao_especial_1 as DATE
cur.execute("ALTER TABLE cnpj_estabelecimentos ADD COLUMN data_situacao_especial_1 DATE")  

# Create a new column data_situacao_especial_2 as string
cur.execute("ALTER TABLE cnpj_estabelecimentos ADD COLUMN data_situacao_especial_2 TEXT")

# Copy the values from data_situacao_especial to data_situacao_especial_1
cur.execute("UPDATE cnpj_estabelecimentos SET data_situacao_especial_2 = data_situacao_especial")

# Change the values in data_situacao_especial_2 to be in the format YYYY-MM-DD
cur.execute("UPDATE cnpj_estabelecimentos SET data_situacao_especial_2 = substr(data_situacao_especial_2, 0, 5) || '-' || substr(data_situacao_especial_2, 5, 2) || '-' || substr(data_situacao_especial_2, 7, 2)")

# Copy the values from data_situacao_especial_2 to data_situacao_especial_1
cur.execute("UPDATE cnpj_estabelecimentos SET data_situacao_especial_1 = data_situacao_especial_2")

# Drop the column data_situacao_especial_2
cur.execute("ALTER TABLE cnpj_estabelecimentos DROP COLUMN data_situacao_especial_2")

# Drop the column data_situacao_especial
cur.execute("ALTER TABLE cnpj_estabelecimentos DROP COLUMN data_situacao_especial")

# Rename the column data_situacao_especial_1 to data_situacao_especial
cur.execute("ALTER TABLE cnpj_estabelecimentos RENAME COLUMN data_situacao_especial_1 TO data_situacao_especial")

# Commit the changes
conn.commit()
"""

"""
# Create a new column called cnpj_completo
cur.execute("ALTER TABLE cnpj_estabelecimentos ADD COLUMN cnpj_completo TEXT")

# make the values of cnpj_completo be "0cnpj_basico/000matriz_filial-cnpj_dv" if cnpj_basico has 7 digits else "cnpj_basico/000matriz_filial-cnpj_dv"
cur.execute("UPDATE cnpj_estabelecimentos SET cnpj_completo = '0' || cnpj_basico_id || '/000' || matriz_filial || '-' || cnpj_dv WHERE length(cnpj_basico_id) = 7")
cur.execute("UPDATE cnpj_estabelecimentos SET cnpj_completo = cnpj_basico_id || '/000' || matriz_filial || '-' || cnpj_dv WHERE length(cnpj_basico_id) = 8")

# Change the values of correio_eletronico to be all lowercase
cur.execute("UPDATE cnpj_estabelecimentos SET correio_eletronico = lower(correio_eletronico)")

# Commit the changes
conn.commit()
"""

"""
# make new column cep_1 as integer
cur.execute("ALTER TABLE cnpj_estabelecimentos ADD COLUMN cep_1 INTEGER")

# make new column cep_2 as text
cur.execute("ALTER TABLE cnpj_estabelecimentos ADD COLUMN cep_2 TEXT")

# make the values of cep_1 be the integer value of cep
cur.execute("UPDATE cnpj_estabelecimentos SET cep_1 = cast(substr(cep, 0, 9) as integer)")

# make the values of cep_2 be the string value of cep_1
cur.execute("UPDATE cnpj_estabelecimentos SET cep_2 = cep_1")

# drop the column cep_1
cur.execute("ALTER TABLE cnpj_estabelecimentos DROP COLUMN cep_1")

# drop the column cep
cur.execute("ALTER TABLE cnpj_estabelecimentos DROP COLUMN cep")

# rename the column cep_2 to cep
cur.execute("ALTER TABLE cnpj_estabelecimentos RENAME COLUMN cep_2 TO cep")

# If a value in cep has 7 digits, add a 0 to the beginning of the value
cur.execute("UPDATE cnpj_estabelecimentos SET cep = '0' || cep WHERE length(cep) = 7")

# Commit the changes
conn.commit()
"""

cur.execute("SELECT cep FROM cnpj_estabelecimentos LIMIT 1")
print(cur.fetchall())

cur.execute("SELECT cep FROM cnpj_estabelecimentos LIMIT 1")
print(cur.fetchall())

# Close the connection
conn.close()