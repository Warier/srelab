from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.database as db_module
from app.database import get_db
from app.main import app


@pytest.fixture
def client(tmp_path: Path) -> Generator[TestClient]:
    """Cria um TestClient com um banco SQLite temporario exclusivo por teste.

    Garante que o lifespan crie as tabelas no banco de teste e limpa os overrides.
    """
    # 1. Cria um arquivo SQLite exclusivo na pasta temporaria fornecida pelo pytest
    db_file = tmp_path / "test_scalepass.db"
    db_url = f"sqlite:///{db_file}"

    # 2. Cria um novo engine e sessionmaker para este teste
    test_engine = create_engine(db_url, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(
        bind=test_engine, autoflush=False, expire_on_commit=False
    )

    # 3. Redireciona o engine global do modulo app.database para usar o engine
    #    de teste. Assim, create_tables() cria as tabelas no banco temporario.
    original_engine = db_module.engine
    db_module.engine = test_engine

    # 4. Define a funcao substituta para a dependencia get_db
    def override_get_db() -> Generator[Session]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # 5. Aplica o override na aplicacao FastAPI
    app.dependency_overrides[get_db] = override_get_db

    # 6. Executa o lifespan usando o TestClient como context manager
    with TestClient(app, follow_redirects=False) as test_client:
        yield test_client

    # 7. Teardown: Restaura o estado original para evitar colateral em outros testes
    app.dependency_overrides.clear()
    db_module.engine = original_engine
