from sqlalchemy import text
from sqlalchemy.orm import Session

from schemas.reports_schemas import FirstReportFields, first_rep_dict, SecondReportFields, second_rep_dict, \
    third_rep_dict, ThirdReportFields, third_rep_medals_dict
from schemas.schemas import FirstReportModel, SecondReportModel, ThirdReportModel


def first_report(
        db: Session,
        form: FirstReportFields
):

    query = """
        SELECT country_name, count(athletes.first_name), olympics.location, olympics.year
        FROM countries
        JOIN athletes ON athletes.country_id = countries.id
        JOIN medals ON athletes.id = medals.athlete_id
        JOIN events ON events.id = medals.event_id
        JOIN olympics ON olympics.id = events.olympic_id 
    """

    query += f"""
        WHERE olympics.year BETWEEN '{form.after}' AND '{form.before}'
    """

    query += f"""
        GROUP BY 1, 3, 4 
        ORDER BY {first_rep_dict[form.sort_column]}
    """

    if form.sort_type == "По убыванию":
        query += " DESC"

    result = [FirstReportModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    report_file = open("C:/Users/Егор/Desktop/Курсовая_БД/reports/report_files/report_1.txt", "w")
    report_file.write("Количество атлетов на олимпиадах по странам\n\n")

    for row in result:
        report_file.write(f"Страна: {row.country_name}\n")
        report_file.write(f"Количество атлетов: {row.count}\n")
        report_file.write(f"Место проведения: {row.location}\n")
        report_file.write(f"Дата начала: {row.year}\n")
        report_file.write("--------------------\n")

    report_file.close()


def second_report(
        db: Session,
        form: SecondReportFields
):
    query = """
        SELECT sports.sport_name, count(events.id), olympics.location, olympics.year
        FROM events
        JOIN sports ON sports.id = events.sport_id
        JOIN olympics ON olympics.id = events.olympic_id
    """

    query += f"""
        WHERE olympics.year BETWEEN '{form.after}' AND '{form.before}'
    """

    query += f"""
        GROUP BY 1, 3, 4 
        ORDER BY {second_rep_dict[form.sort_column]}
    """

    if form.sort_type == "По убыванию":
        query += " DESC"

    result = [SecondReportModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    report_file = open("C:/Users/Егор/Desktop/Курсовая_БД/reports/report_files/report_2.txt", "w")
    report_file.write("Количество событий по каждому виду спорта на олимпиалдах\n\n")

    for row in result:
        report_file.write(f"Вид спорта: {row.sport_name}\n")
        report_file.write(f"Количество событий: {row.count}\n")
        report_file.write(f"Место проведения: {row.location}\n")
        report_file.write(f"Дата начала: {row.year}\n")
        report_file.write("--------------------\n")

    report_file.close()

def third_report(
        db: Session,
        form: ThirdReportFields
):
    query = """
            SELECT last_name, first_name, count(medals.id)
            FROM athletes
            JOIN medals ON medals.athlete_id = athletes.id
            JOIN events ON medals.event_id = events.id
        """

    if form.medal_type:
        query += f"""
                WHERE medals.medal_type = {form.medal_type}'
            """

    query += f"""
            GROUP BY 1, 2
            ORDER BY {third_rep_dict[form.sort_column]}
        """

    if form.sort_type == "По убыванию":
        query += " DESC"

    result = [ThirdReportModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    report_file = open("C:/Users/Егор/Desktop/Курсовая_БД/reports/report_files/report_3.txt", "w")
    report_file.write(f"Количество {third_rep_medals_dict[form.medal_type] if form.medal_type else ''} "
                      f"медалей каждого атлета\n\n")

    for row in result:
        report_file.write(f"Фамилия: {row.last_name}\n")
        report_file.write(f"Имя: {row.first_name}\n")
        report_file.write(f"Количество медалей: {row.count}\n")
        report_file.write("--------------------\n")

    report_file.close()

