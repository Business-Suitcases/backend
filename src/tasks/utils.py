from sqlalchemy import Result


def res_to_dict(res: Result) -> list[dict]:
    row = res.fetchall()
    return [row._asdict() for row in row]
