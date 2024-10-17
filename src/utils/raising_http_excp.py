from fastapi import HTTPException
from starlette import status


class RaiseHttpException:

    @staticmethod
    def check_is_exist(item):
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )
