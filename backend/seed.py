import asyncio
from datetime import datetime
from database import db
from auth import get_password_hash

async def seed():
    # 1. Clear database
    await db.categories.delete_many({})
    await db.artworks.delete_many({})
    await db.users.delete_many({})
    await db.orders.delete_many({})

    # 2. Seed Categories
    await db.categories.insert_many([
        {'name': 'Peinture'},
        {'name': 'Sculpture'},
        {'name': 'Digital Art'},
        {'name': 'Photographie'}
    ])

    # 3. Seed Users
    admin_id = 'admin_id_mocked'
    artist_id = 'artist_id_mocked'
    user_id = 'user_id_mocked'
    
    users_to_seed = [
        {
            '_id': admin_id,
            'email': 'admin@egallery.com',
            'username': 'Larry (Admin)',
            'role': 'admin',
            'password': get_password_hash('admin123')
        },
        {
            '_id': artist_id,
            'email': 'artist@egallery.com',
            'username': 'Vincent Van Gogh (Artist)',
            'role': 'artist',
            'password': get_password_hash('artist123')
        },
        {
            '_id': user_id,
            'email': 'user@egallery.com',
            'username': 'Claude Monet (User)',
            'role': 'user',
            'password': get_password_hash('user123')
        }
    ]
    await db.users.insert_many(users_to_seed)

    # 4. Seed Artworks
    await db.artworks.insert_many([
        {
            'title': 'Le Secret des Etoiles',
            'description': 'Une œuvre digitale capturant la beauté fugace d\'une nébuleuse lointaine.',
            'price': 1200.0,
            'category': 'Digital Art',
            'image_url': 'https://images.unsplash.com/photo-1464802686167-b939a6910659?q=80&w=1200&auto=format&fit=crop',
            'author_id': artist_id,
            'author_name': 'Vincent Van Gogh (Artist)',
            'is_sold': False,
            'created_at': datetime.utcnow()
        },
        {
            'title': 'Sérénité de Marbre',
            'description': 'Sculpture minimaliste représentant l\'équilibre parfait entre force et douceur.',
            'price': 4500.0,
            'category': 'Sculpture',
            'image_url': 'https://images.unsplash.com/photo-1554188248-986adbb73be4?q=80&w=1200&auto=format&fit=crop',
            'author_id': artist_id,
            'author_name': 'Vincent Van Gogh (Artist)',
            'is_sold': False,
            'created_at': datetime.utcnow()
        },
        {
            'title': 'Eclat d\'Automne',
            'description': 'Peinture à l\'huile sur toile, capturant les couleurs vibrantes d\'une forêt en octobre.',
            'price': 2800.0,
            'category': 'Peinture',
            'image_url': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?q=80&w=1200&auto=format&fit=crop',
            'author_id': admin_id,
            'author_name': 'Larry (Admin)',
            'is_sold': False,
            'created_at': datetime.utcnow()
        }
    ])
    print("Database cleared and seeded with default categories, users (admin@egallery.com / artist@egallery.com / user@egallery.com), and mock artworks.")

if __name__ == "__main__":
    asyncio.run(seed())

