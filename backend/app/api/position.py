from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import require_permission
from app.models.position import Position
from app.models.permission import Permission
from app.schemas.position import PositionCreate, PositionResponse, PositionUpdate

router = APIRouter()


@router.post("/", response_model=PositionResponse)
def create_position(
    position: PositionCreate,
    permission=Depends(require_permission("create_position")),
    db: Session = Depends(get_db),
):
    permissions = (
        db.query(Permission).filter(Permission.id.in_(position.permissions_ids)).all()
    )

    db_position = Position(name=position.name, permissions=permissions)

    db.add(db_position)
    db.commit()
    db.refresh(db_position)

    return db_position


@router.put("/{position_id}", response_model=PositionResponse)
def update_position(
    position_id: int,
    position: PositionUpdate,
    permission=Depends(require_permission("update_position")),
    db: Session = Depends(get_db),
):
    position_to_update = db.query(Position).filter(Position.id == position_id).first()

    if not position_to_update:
        raise HTTPException(status_code=404, detail="Position not found")

    if position.name is not None:
        position_to_update.name = position.name

    if position.permissions_ids is not None:
        permissions = (
            db.query(Permission)
            .filter(Permission.id.in_(position.permissions_ids))
            .all()
        )
        position_to_update.permissions = permissions

    db.commit()
    db.refresh(position_to_update)

    return position_to_update


@router.get("/", response_model=list[PositionResponse])
def get_positions(
    permission=Depends(require_permission("view_position")),
    db: Session = Depends(get_db),
):
    positions = db.query(Position).all()

    return positions


@router.get("/{position_id}", response_model=PositionResponse)
def get_position(
    position_id: int,
    permission=Depends(require_permission("view_position")),
    db: Session = Depends(get_db),
):
    position = db.query(Position).filter(Position.id == position_id).first()

    if not position:
        raise HTTPException(status_code=404, detail="Cargo não encontrado.")

    return position


@router.delete("/{position_id}")
def delete_position(
    position_id: int,
    permission=Depends(require_permission("delete_position")),
    db: Session = Depends(get_db),
):
    position = db.query(Position).filter(Position.id == position_id).first()

    if not position:
        raise HTTPException(status_code=404, detail="Cargo não encontrado.")

    db.delete(position)
    db.commit()

    return {"message": "Cargo deletado com sucesso."}


@router.delete("/list/delete")
def delete_position_list(
    position_ids: list[int],
    permission=Depends(require_permission("delete_position")),
    db: Session = Depends(get_db),
):
    positions = db.query(Position).filter(Position.id.in_(position_ids)).all()
    for position in positions:
        db.delete(position)
        db.commit()
    return {"message": "Cargos deletados com sucesso."}
