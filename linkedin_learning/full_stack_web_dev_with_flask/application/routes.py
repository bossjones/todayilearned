from application import app, db
from flask import (
    render_template,
    request,
    json,
    Response,
    redirect,
    flash,
    url_for,
    session,
)
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

usersData = [
    {
        "id": 1,
        "first_name": "Jacques",
        "last_name": "Blazewicz",
        "email": "jblazewicz0@posterous.com",
        "password": "k9doaly",
    },
    {
        "id": 2,
        "first_name": "Budd",
        "last_name": "Zellick",
        "email": "bzellick1@uol.com.br",
        "password": "kik8N0cyKG",
    },
    {
        "id": 3,
        "first_name": "Simone",
        "last_name": "Brenston",
        "email": "sbrenston2@squarespace.com",
        "password": "9BO7nEvdci8",
    },
    {
        "id": 4,
        "first_name": "Waneta",
        "last_name": "Stading",
        "email": "wstading3@google.es",
        "password": "GpzWY536X",
    },
    {
        "id": 5,
        "first_name": "Barbey",
        "last_name": "Corder",
        "email": "bcorder4@csmonitor.com",
        "password": "BXFkbgEz",
    },
    {
        "id": 6,
        "first_name": "Becca",
        "last_name": "Hartington",
        "email": "bhartington5@wsj.com",
        "password": "ijh3RfxcGB",
    },
    {
        "id": 7,
        "first_name": "Elyse",
        "last_name": "Eddy",
        "email": "eeddy6@archive.org",
        "password": "QJHg5Gc0V",
    },
    {
        "id": 8,
        "first_name": "Reggie",
        "last_name": "Souster",
        "email": "rsouster7@4shared.com",
        "password": "nmCeQGRC",
    },
    {
        "id": 9,
        "first_name": "Brnaby",
        "last_name": "Abrahmson",
        "email": "babrahmson8@digg.com",
        "password": "BqOgwfIMJmTx",
    },
    {
        "id": 10,
        "first_name": "Yuma",
        "last_name": "Graine",
        "email": "ygraine9@tmall.com",
        "password": "4VpkAWyL",
    },
    {
        "id": 11,
        "first_name": "Quinton",
        "last_name": "Chater",
        "email": "qchatera@squarespace.com",
        "password": "7x6IYp",
    },
    {
        "id": 12,
        "first_name": "Raymund",
        "last_name": "Moorman",
        "email": "rmoormanb@indiatimes.com",
        "password": "aRgaXm1",
    },
    {
        "id": 13,
        "first_name": "Boycey",
        "last_name": "Ferrelli",
        "email": "bferrellic@cnet.com",
        "password": "VCKtIJEUi",
    },
    {
        "id": 14,
        "first_name": "Ty",
        "last_name": "Raffeorty",
        "email": "traffeortyd@cnet.com",
        "password": "wVOd2oi",
    },
    {
        "id": 15,
        "first_name": "Judie",
        "last_name": "Penella",
        "email": "jpenellae@psu.edu",
        "password": "0WP0F6516",
    },
    {
        "id": 16,
        "first_name": "Alden",
        "last_name": "Gemlett",
        "email": "agemlettf@independent.co.uk",
        "password": "3rAW4wlTsCWz",
    },
    {
        "id": 17,
        "first_name": "Josephina",
        "last_name": "MacLeod",
        "email": "jmacleodg@livejournal.com",
        "password": "gQ7ytj7CtA6",
    },
    {
        "id": 18,
        "first_name": "Lorene",
        "last_name": "Lindeberg",
        "email": "llindebergh@chron.com",
        "password": "Q4WU8aHkm",
    },
    {
        "id": 19,
        "first_name": "Lamar",
        "last_name": "Sotham",
        "email": "lsothami@rediff.com",
        "password": "5yyhnYPTDs",
    },
    {
        "id": 20,
        "first_name": "Derek",
        "last_name": "Breakey",
        "email": "dbreakeyj@home.pl",
        "password": "jrz2kl2jeX",
    },
]

_courseData = [
    {
        "courseID": "1111",
        "title": "PHP 111",
        "description": "Intro to PHP",
        "credits": "3",
        "term": "Fall, Spring",
    },
    {
        "courseID": "2222",
        "title": "Java 1",
        "description": "Intro to Java Programming",
        "credits": "4",
        "term": "Spring",
    },
    {
        "courseID": "3333",
        "title": "Adv PHP 201",
        "description": "Advanced PHP Programming",
        "credits": "3",
        "term": "Fall",
    },
    {
        "courseID": "4444",
        "title": "Angular 1",
        "description": "Intro to Angular",
        "credits": "3",
        "term": "Fall, Spring",
    },
    {
        "courseID": "5555",
        "title": "Java 2",
        "description": "Advanced Java Programming",
        "credits": "4",
        "term": "Fall",
    },
]


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    # if already logged in, redirect to homepage
    if session.get("username"):
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # compare email in db against one in form
        user = User.objects(email=email).first()

        if user and user.get_password(password):
            flash(f"{user.first_name}, you are sucessfully logged in!", "success")
            session["user_id"] = user.user_id
            session["username"] = user.first_name
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/logout")
def logout():
    session["user_id"] = False
    session.pop("username", None)
    return redirect("/index")


@app.route("/courses")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "Spring 2019"
    classes = Course.objects.order_by("-courseID")
    return render_template("courses.html", courseData=classes, courses=True, term=term)


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        # count the amount of data in db ( use this to auto create id for mongo )
        user_id = User.objects.count()
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(
            user_id=user_id, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.save()
        flash("You are successfully registered!", "success")
        return redirect((url_for("index")))

    return render_template("register.html", title="Register", form=form, register=True)


# SOURCE: https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    # if already logged in, redirect to homepage
    if not session.get("username"):
        return redirect(url_for("login"))

    # only see enrollment if you are logged in

    # form.get = less strict, if you have courseID return it, otherwise None
    courseID = request.form.get("courseID")
    # request.form["<VALUE>"] is strict, if you don't have it, app will throw stack trace
    # title = request.form["title"]
    courseTitle = request.form.get("title")
    user_id = session.get("user_id")

    # if you're coming from enrollment page, we don't need ot add anything
    if courseID:
        # then we can process the enrollment
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(
                f"Oops! You are already registered in this course {courseTitle}!",
                "danger",
            )
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You enrolled in {courseTitle}!", "success")

    classes = list(
        User.objects.aggregate(
            *[
                {
                    "$lookup": {
                        "from": "enrollment",
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "r1",
                    }
                },
                {
                    "$unwind": {
                        "path": "$r1",
                        "includeArrayIndex": "r1_id",
                        "preserveNullAndEmptyArrays": False,
                    }
                },
                {
                    "$lookup": {
                        "from": "course",
                        "localField": "r1.courseID",
                        "foreignField": "courseID",
                        "as": "r2",
                    }
                },
                {"$unwind": {"path": "$r2", "preserveNullAndEmptyArrays": False}},
                {"$match": {"user_id": user_id}},
                {"$sort": {"courseID": 1}},
            ]
        )
    )

    return render_template(
        "enrollment.html", enrollment=True, title="Enrollment", classes=classes
    )


@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    courseData = Course.objects.order_by("courseID")
    if idx == None:
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


@app.route("/user")
def user():
    users = User.objects.all()
    return render_template("user.html", users=users)


def _fixtures():
    for i in usersData:
        user = User(
            user_id=i["id"],
            email=i["email"],
            first_name=i["first_name"],
            last_name=i["last_name"],
        )
        user.set_password(i["password"])
        user.save()


def _fixtures_courses():
    for i in _courseData:
        Course(
            courseID=i["courseID"],
            title=i["title"],
            description=i["description"],
            credits=i["credits"],
            term=i["term"],
        ).save()


@app.route("/fixtures")
def fixtures():
    _fixtures()
    _fixtures_courses()
    users = User.objects.all()
    return Response(json.dumps(users), mimetype="application/json")
