from fastapi import APIRouter, Query, HTTPException
from fastapi.params import Depends
from sqlalchemy import Select
from sqlmodel import Session, select,func
from models import Reviews,ReviewCreate,ReviewUpdate,ReadReview
from database import get_session

router=APIRouter(prefix="/review", tags=["Review"])
# tag is used to show all request under review


# this file is create to code moduler

@router.post("/",response_model=ReadReview)
def create_review(review:ReviewCreate, session:Session=Depends(get_session)):
    # Session=Depends(get_session() is actually direct dependency injection in fastapi
    db_review=Reviews(**review.model_dump()) # this is just python, it is unpacking os a dictionary
    #model dump convert pydantic object in dictionary
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


@router.get("/",response_model=list[ReadReview])
def list_reviews(
        play_name:str| None= Query(None,description="Filter by play name"),
        skip:int =Query(0,description="Number of reviews to skip"),
        limit:int =Query(1,description="Max reviews to return"),
        session:Session=Depends(get_session)):
    #skip and limit used in pagination -> how many records you want to see on the page

    query=select(Reviews)  # selecting a table

    if play_name:
        query=query.where(Reviews.play_name == play_name)
    query =query.offset(skip).limit(limit)  # this takes care of [pagination
    reviews=session.exec(query).all()
    return reviews

@router.get("/average/{play_name}")
def get_average_rating(play_name:str, session:Session=Depends(get_session)):
    result=session.exec(
        select(func.avg(Reviews.rating),func.count(Reviews.id)).where(
            Reviews.play_name == play_name
        )
    ).first()

    # it is required to do first or all because then only value will be returned
    avg_rating,total_reviews=result
    if total_reviews==0:
        raise HTTPException(status_code=404, detail="No review found")
    return{
        "play_name": play_name,
        "average_rating" :round(avg_rating,2),
        "total_reviews": total_reviews
    }


@router.patch("/{review_id}",response_model=ReadReview)
def update_review(review_id:int, update:ReviewUpdate,session:Session=Depends(get_session)):
    review=session.get(Reviews,review_id)
    if not review :
        raise HTTPException(status_code=400,detail="No review present with review id ")

    update_data=update.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(review,key,value)
    # this is pure python which will update dictionary

    session.add(review)
    session.commit()
    session.refresh(review)
    return review

@router.delete("/{review_id}")
def delete_review(review_id:int,session:Session=Depends(get_session)):
    review=session.get(Reviews,review_id)
    if not review :
        raise HTTPException(status_code=400,detail="No review present with review id ")

    session.delete(review)
    session.commit()
    return {
        "message":"Delete review"
    }


@router.delete("/delete/{play_name}")
def delete_all_review(play_name:str,session:Session=Depends(get_session)):
    query=select(Reviews)
    query =query.where(Reviews.play_name==play_name)
    result=session.exec(query).all()
    total_reviews=len(result)
    # result=session.exec(select(Reviews).where(Reviews.play_name==play_name)).all()
    if total_reviews:
        raise HTTPException(status_code=400, detail=" No reviews found with play_name")
    for review in result:
        session.delete(review)
        session.commit()

    return {
        "message":f'{total_reviews} review deleted for {play_name}'
    }