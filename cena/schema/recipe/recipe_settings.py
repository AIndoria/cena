from cena.schema._cena import CenaModel


class RecipeSettings(CenaModel):
    public: bool = False
    show_nutrition: bool = False
    show_assets: bool = False
    landscape_view: bool = False
    disable_comments: bool = True
    disable_amount: bool = True
    locked: bool = False

    class Config:
        orm_mode = True
