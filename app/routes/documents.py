
import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.document import Document
from app.schemas.document_schema import DocumentResponse
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.auth import get_current_user, admin_only
from app.models.status_history import DocumentStatusHistory
from fastapi import BackgroundTasks

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def send_approval_notification(document_id: int):
    print(f"Document {document_id} approved. Email sent to user.")


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # Validate file type
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only PDF and images allowed")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    new_doc = Document(
        filename=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc


@router.get("/my-documents", response_model=list[DocumentResponse])
def get_my_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Document).filter(
        Document.uploaded_by == current_user.id
    ).all()

@router.post("/approve/{doc_id}")
def approve_document(
    doc_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin = Depends(admin_only)
):
    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.status = "approved"

    # Save history
    history = DocumentStatusHistory(
        document_id=document.id,
        status="approved"
    )

    db.add(history)
    db.commit()

    background_tasks.add_task(
        send_approval_notification,
        document.id
    )

    return {"message": "Document approved"}


@router.post("/reject/{doc_id}")
def reject_document(
    doc_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_only)
):
    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    document.status = "rejected"

    history = DocumentStatusHistory(
        document_id=document.id,
        status="rejected"
    )

    db.add(history)
    db.commit()

    return {"message": "Document rejected"}


@router.get("/all-documents")
def get_all_documents(
    db: Session = Depends(get_db),
    admin = Depends(admin_only)
):
    return db.query(Document).all()

@router.get("/documents")
def get_documents(
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Document)

    if status:
        query = query.filter(Document.status == status)

    total = query.count()

    offset = (page - 1) * limit

    documents = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": documents
    }