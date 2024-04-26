import asyncpg
import asyncio

async def test_database_connection():
    try:
        # Verbinding maken met de database
        connection = await asyncpg.connect(DATABASE_URL)

        # Een eenvoudige query uitvoeren om de databaseversie op te halen
        version = await connection.fetchval("SELECT version();")
        print("Database version:", version)

    except Exception as e:
        print("Er is een fout opgetreden bij het verbinden met de database:", e)

    finally:
        # De verbinding sluiten
        await connection.close()

# Voer de testfunctie uit binnen een event loop
async def main():
    await test_database_connection()

# Start de event loop om de test uit te voeren
if __name__ == "__main__":
    asyncio.run(main())
