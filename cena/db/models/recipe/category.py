import sqlalchemy as sa
import sqlalchemy.orm as orm
from cena.core import root_logger
from cena.db.models.model_base import SqlAlchemyBase
from slugify import slugify
from sqlalchemy.orm import validates

logger = root_logger.get_logger()

site_settings2categories = sa.Table(
    "site_settings2categories",
    SqlAlchemyBase.metadata,
    sa.Column("site_settings.id", sa.Integer, sa.ForeignKey("site_settings.id")),
    sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")),
)

group2categories = sa.Table(
    "group2categories",
    SqlAlchemyBase.metadata,
    sa.Column("group_id", sa.Integer, sa.ForeignKey("groups.id")),
    sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")),
)

recipes2categories = sa.Table(
    "recipes2categories",
    SqlAlchemyBase.metadata,
    sa.Column("recipe_id", sa.Integer, sa.ForeignKey("recipes.id")),
    sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")),
)

custom_pages2categories = sa.Table(
    "custom_pages2categories",
    SqlAlchemyBase.metadata,
    sa.Column("custom_page_id", sa.Integer, sa.ForeignKey("custom_pages.id")),
    sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")),
)


class Category(SqlAlchemyBase):
    __tablename__ = "categories"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, index=True, nullable=False)
    slug = sa.Column(sa.String, index=True, unique=True, nullable=False)
    recipes = orm.relationship("RecipeModel", secondary=recipes2categories, back_populates="recipe_category")

    @validates("name")
    def validate_name(self, key, name):
        assert name != ""
        return name

    def __init__(self, name, session=None) -> None:
        self.name = name.strip()
        self.slug = slugify(name)

    def update(self, name, session=None) -> None:
        self.__init__(name, session)

    @staticmethod
    def get_ref(session, slug: str):
        return session.query(Category).filter(Category.slug == slug).one()

    @staticmethod
    def create_if_not_exist(session, name: str = None):
        test_slug = slugify(name)
        result = session.query(Category).filter(Category.slug == test_slug).one_or_none()
        if result:
            logger.debug("Category exists, associating recipe")
            return result
        else:
            logger.debug("Category doesn't exists, creating tag")
            return Category(name=name)
