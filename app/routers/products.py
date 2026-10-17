from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse, ProductUpdate


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """GET /products - Lấy danh sách tất cả sản phẩm"""
    return db.query(Product).order_by(Product.id).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """GET /products/{id} - Lấy chi tiết một sản phẩm"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sản phẩm có id = {product_id}"
        )
    return product


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """POST /products - Thêm sản phẩm mới"""
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        quantity=product_data.quantity,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    """PUT /products/{id} - Cập nhật thông tin sản phẩm"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sản phẩm có id = {product_id}"
        )

    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """DELETE /products/{id} - Xóa sản phẩm"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sản phẩm có id = {product_id}"
        )

    db.delete(product)
    db.commit()
    return {"message": f"Đã xóa sản phẩm có id = {product_id}"}