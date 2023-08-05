# Copyright 2020 John Reese
# Licensed under the MIT License

import click

from multiflash.common import find_numbers, natural_sort
from multiflash.dataset import Fact, Facts, connect, set_default
from multiflash.question import FillKeyword
from multiflash.quiz import Quiz, QuizError


@click.group(context_settings={"help_option_names": ["-h", "--help"]},)
@click.option(
    "--db",
    help="location of dataset",
    type=click.Path(dir_okay=False, file_okay=True, writable=True, resolve_path=True),
    default=None,
)
@click.pass_context
def multiflash(ctx, db):
    """Interact with the multiflash database"""
    if db is not None:
        set_default(db)


@multiflash.command("add")
def add():
    """Add new facts to the dataset"""
    db, engine = connect()

    query = Facts.select(Facts.class_name)
    cursor = db.execute(*engine.prepare(query))
    rows = cursor.fetchall()
    if rows:
        class_name = rows[-1]["class_name"]
    else:
        class_name = ""
    class_name = click.prompt("Class name", default=class_name).strip()

    query = Facts.select(Facts.topic).where(Facts.class_name == class_name)
    cursor = db.execute(*engine.prepare(query))
    rows = cursor.fetchall()
    if rows:
        topic = rows[-1]["topic"]
    else:
        topic = ""
    topic = click.prompt("Topic", default=topic).strip()

    while True:
        keyword = input("\n  Keyword [done]: ").strip()
        if not keyword:
            break
        description = click.prompt("    Description").strip()

        values = set()
        while True:
            value = input("    Value [done]: ").strip()
            if not value:
                break
            values.add(value)

        try:
            fact = Fact(class_name, topic, keyword, description, "|||".join(values))
            query = Facts.insert().values(fact)
            db.execute(*engine.prepare(query))
            db.commit()
        except Exception as e:
            click.echo(f"Failed to add fact: {e}")


@multiflash.command("list")
@click.argument("class_name", required=False, default=None)
def list(class_name):
    """List facts"""
    db, engine = connect()
    query = Facts.select()
    if class_name:
        query.where(Facts.class_name == class_name)
    sql, parameters = engine.prepare(query)
    sql += " ORDER BY class_name ASC, topic ASC, keyword ASC"
    cursor = db.execute(*engine.prepare(query))
    for row in cursor:
        fact = Fact(**row)
        print(
            f"{fact.class_name} | {fact.topic} | {fact.keyword} | "
            f"{fact.description} | {fact.values}"
        )


@multiflash.command("quiz")
@click.argument("class_name", required=False)
@click.option("--harder", is_flag=True, help="Don't show any choices")
@click.option("--limit", type=int, default=None, help="Maximum number of questions")
def quiz(class_name, harder, limit):
    """Take a quiz"""
    if not class_name:
        db, engine = connect()
        query = Facts.select(Facts.class_name).groupby(Facts.class_name)
        cursor = db.execute(*engine.prepare(query))
        rows = cursor.fetchall()
        class_names = sorted(row["class_name"] for row in rows)
        if not class_names:
            click.echo("Add some facts first")
            click.exit()

        if len(class_names) == 1:
            class_name = class_names[0]
        else:
            class_name = click.prompt("Class name", type=click.Choice(class_names))

    query = (
        Facts.select(Facts.topic)
        .groupby(Facts.topic)
        .where(Facts.class_name == class_name)
    )
    cursor = db.execute(*engine.prepare(query))
    rows = cursor.fetchall()
    topics = dict(
        enumerate(sorted((row["topic"] for row in rows), key=natural_sort), start=1)
    )
    chosen = []
    while not chosen:
        click.echo(f"Known topics for {class_name}:\n")
        for number, name in topics.items():
            click.echo(f"  {number:>3}: {name}")
        selection = click.prompt("\nChoose topics", default="all").strip()
        if selection == "all":
            break
        chosen = find_numbers(selection)
        if not chosen:
            click.secho(
                "Unknown selection, enter numbers separated by commas", fg="red"
            )
    topic_list = [topics[k] for k in chosen]

    try:
        if harder:
            quiz = Quiz(
                class_name,
                topic_list=topic_list,
                question_limit=limit,
                question_types=[FillKeyword],
            )
        else:
            quiz = Quiz(class_name, topic_list=topic_list, question_limit=limit)

        quiz.start()

    except QuizError as e:
        click.secho(str(e), fg="red")


@multiflash.command("gui")
def gui():
    """Start the Multiflash GUI"""
    from multiflash.gui import start

    start()


if __name__ == "__main__":
    multiflash(prog_name="multiflash")  # pylint: disable=all
