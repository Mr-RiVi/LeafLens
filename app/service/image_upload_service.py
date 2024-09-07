from app.model.image_model import Image
from app import db

def save_image(filename, project_id, image_url):
    """Saves image metadata to the database."""
    image = Image(filename=filename, project_id=project_id, image_url=image_url)
    db.session.add(image)
    db.session.commit()
    return image

def get_image(image_id):
    """Fetches an image by its ID."""
    return db.session.query(Image).filter_by(image_id=image_id).first()

def get_all_images():
    """Fetches all images from the database."""
    return db.session.query(Image).all()

def delete_image(image_id):
    """Deletes an image by its ID."""
    image = get_image(image_id)
    if image:
        db.session.delete(image)
        db.session.commit()
        return True
    return False
