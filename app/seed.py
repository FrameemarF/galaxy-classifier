from app.database.database import Session, engine
from app.models.galaxy_class import GalaxyClassDB
from sqlalchemy import select

GALAXIES = [{
        "model_index": 0,
        "name": "Disturbed Galaxies",
        "description": "Галактика с искажённой, асимметричной формой — обычно результат гравитационного взаимодействия с соседней галактикой" 
    },
    {
        "model_index": 1,
        "name": "Merging Galaxies",
        "description": "Две (или больше) галактики, находящиеся в процессе слияния — видны признаки перекрывающихся структур"
    },
    {
        "model_index": 2,
        "name": "Round Smooth Galaxies",
        "description": "Гладкая, идеально круглая галактика без видимых структурных деталей (рукавов, дисков)"
    },
    {
        "model_index": 3,
        "name": "In-between Round Smooth Galaxies",
        "description": "Гладкая галактика промежуточной, слегка вытянутой формы — между идеально круглой и сигарообразной"
    },
    {
        "model_index": 4,
        "name": "Cigar Shaped Smooth Galaxies",
        "description": "Гладкая, сильно вытянутая (сигарообразная) галактика без видимой спиральной структуры"
    },
    {
        "model_index": 5,
        "name": "Barred Spiral Galaxies",
        "description": "Спиральная галактика с чётко выраженной центральной перемычкой (баром), от которой отходят рукава"
    },
    {
        "model_index": 6,
        "name": "Unbarred Tight Spiral Galaxies",
        "description": "Спиральная галактика без перемычки, с плотно закрученными рукавами"
    },
    {
        "model_index": 7,
        "name": "Unbarred Loose Spiral Galaxies",
        "description": "Спиральная галактика без перемычки, с широко раскрученными, рыхлыми рукавами"
    },
    {
        "model_index": 8,
        "name": "Edge-on Galaxies without Bulge",
        "description": "Галактика, видимая с ребра (плашмя), без заметного центрального утолщения (балджа)"
    },
    {
        "model_index": 9,
        "name": "Edge-on Galaxies with Bulge",
        "description": "Галактика, видимая с ребра, с выраженным центральным утолщением (балджем)"
    }
]

def seed():
    with Session(engine) as session:
        if session.scalar(select(GalaxyClassDB).limit(1)) is not None:
            print("galaxies already seeded, skip")
            return

        session.add_all([GalaxyClassDB(**g) for g in GALAXIES])
        session.commit()
        print(f"seeded {len(GALAXIES)} galaxy classes")


if __name__ == "__main__":
    seed()