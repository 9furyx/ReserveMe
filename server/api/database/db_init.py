from api.database.database import db
from api.models import User

def create_admin_user():
    user = User.query.filter_by(email='admin@example.com').first()
    if user is None:
        user = User(username='admin', password='sha256$iXFvwRru$1a27f78f6b54856229bd8def21e5dc1d972cb19fc28c5b023917a25525bfaed0',
                   email='admin@example.com', user_role='admin')

        db.session.add(user)
        db.session.commit()