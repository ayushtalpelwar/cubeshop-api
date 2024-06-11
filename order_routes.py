from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from model import User,Order
from schemas import OrderModel,OrderStatusModel
from fastapi.exceptions import HTTPException
from database import Session,engine
from fastapi.encoders import jsonable_encoder

order_router=APIRouter(prefix="/order",tags=['order'])

session=Session(bind=engine)

@order_router.get("/")
async def hello(Authorize:AuthJWT=Depends()):
    """
    ## A sample hello world route
    This returns Hello world
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    return {"message":"Hello World"}



@order_router.post("/order",status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        dimensions=order.dimensions,
        quantity=order.quantity
    )

    new_order.user=user

    session.add(new_order)

    session.commit()

    response={
        "dimensions":new_order.dimensions,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)

@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token re")

    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders=session.query(Order).all()
        return jsonable_encoder(orders)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not SuperUser")


@order_router.get('/order/{id}')
async def get_order(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token re")

    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()
        return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not Allowed")

@order_router.get('/user/orders')
async def get_user_order(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token re")

    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)
    

@order_router.get('/user/order/{id}/')
async def get_user_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    subject=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==subject).first()

    orders=current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )


@order_router.put('/order/update/{id}/')
async def update_order(id:int,order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    order_to_update=session.query(Order).filter(Order.id==id).first()
    
    order_to_update.quantity=order.quantity
    order_to_update.dimensions=order.dimensions

    session.commit()

    return jsonable_encoder(order_to_update)

@order_router.patch('/order/status/{id}')
async def update_order_status(id:int,order:OrderStatusModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token r")

    username=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()

        order_to_update.order_status=order.order_status

        session.commit()

        response={
            "id":order_to_update.id,
            "quantity":order_to_update.quantity,
            "dimensions":order_to_update.dimensions,
            "order_status":order_to_update.order_status
        }
        return jsonable_encoder(response)
    

@order_router.delete('/order/delete/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token r")

    order_to_delete=session.query(Order).filter(Order.id==id).first()

    session.delete(order_to_delete)
    session.commit()
    return jsonable_encoder(order_to_delete)