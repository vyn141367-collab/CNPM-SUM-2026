from sqlalchemy.orm import Session
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from infrastructure.models.submission_model import SubmissionModel

class SubmissionRepository:
    def __init__(self, session: Session = None):
        if session is None:
            self.session = db_factory.get_database('POSTGREE').get_session()
        else:
            self.session = session

    def create_submission(self, data: dict) -> SubmissionModel:
        try:
            new_submission = SubmissionModel(
                title=data.get('title'),
                image_url=data.get('image_url'),
                film_stock=data.get('film_stock'),
                camera=data.get('camera'),
                lens=data.get('lens'),
                iso=data.get('iso'),
                film_format=data.get('film_format'),
                developing_lab=data.get('developing_lab'),
                scanning_specs=data.get('scanning_specs')
            )
            self.session.add(new_submission)
            self.session.commit()
            self.session.refresh(new_submission)
            return new_submission
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_all(self):
        try:
            return self.session.query(SubmissionModel).all()
        finally:
            self.session.close()

    def update_submission(self, sub_id, data: dict):
        try:
            numeric_id = int(sub_id)
            submission = self.session.query(SubmissionModel).filter(SubmissionModel.id == numeric_id).first()
            if not submission:
                raise Exception(f"Không tìm thấy bài thi có ID {sub_id}")

            if 'title' in data and data['title']:
                submission.title = data['title']
            if 'camera' in data and data['camera']:
                submission.camera = data['camera']
            if 'film_stock' in data and data['film_stock']:
                submission.film_stock = data['film_stock']
            if 'film_format' in data and data['film_format']:
                submission.film_format = data['film_format']

            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def delete_submission(self, sub_id):
        try:
            numeric_id = int(sub_id)
            submission = self.session.query(SubmissionModel).filter(SubmissionModel.id == numeric_id).first()
            if not submission:
                raise Exception(f"Không tìm thấy bài thi có ID {sub_id} trong Database!")

            self.session.delete(submission)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()