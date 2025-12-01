from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt
from app.db import fetch_all

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/",
    template_folder="../../frontEnd",
    static_folder="../../frontEnd",
)


@main_bp.route("/profile")
@jwt_required()
def profile():
    claims = get_jwt()
    role = claims.get('role')

    if role == 'tatuador':
        return redirect(url_for('main.tattooer_page'))
    
    # Clientes ou qualquer outro caso vão para a página de usuário padrão
    return redirect(url_for('main.user_page'))


@main_bp.route("/")
def root():
    return render_template("account.html")


@main_bp.route("/login")
def login():
    return render_template("account.html")


@main_bp.route("/home")
def home():
    query = "SELECT id_tatuador, nome, foto_url FROM tatuador ORDER BY id_tatuador ASC LIMIT 5"
    artistas_destaque = fetch_all(query)
    return render_template("index.html", artistas_destaque=artistas_destaque)


@main_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@main_bp.route("/user")
def user_page():
    return render_template("user.html")


@main_bp.route("/search")
def search_page():
    return render_template("search.html")


@main_bp.route("/tattooer")
def tattooer_page():
    return render_template("tattooer.html")


@main_bp.route("/tattooer/<int:tatuador_id>")
def tattooer_page_id(tatuador_id):
    return render_template("tattooer.html", tatuador_id=tatuador_id)


@main_bp.route("/sobre-contato")
def about_page():
    return render_template("sobreContato.html")


styles_data = {
    "blackwork": {
        "title": "BLACKWORK",
        "description": "O mais <strong>dark</strong> dos estilos de tatu, o Blackwork é puro preto e impacto. Usando <strong>apenas tinta preta</strong>, ele cria <strong>contrastes marcantes</strong> com designs que vão do tribal ao geométrico, do ornamental ao blackout (cobertura total). Ideal para quem quer um visual ousado e atemporal, com <strong>linhas precisas e sombras intensas.</strong> Dura muito tempo... e é certeza de deixar aquele impacto que você merece 🖤",
        "image": "blackwork-bg.png",
        "sub_styles": [
            {"name": "geometric", "title": "Geométrico", "image": "geometric-bg.jpg"},
            {"name": "fineline", "title": "Fineline", "image": "fineline-bg.jpg"}
        ]
    },
    "fineline": {
        "title": "FINELINE",
        "description": "O estilo <strong>Fineline</strong>, ou traço fino, é a pura expressão da <strong>delicadeza</strong> e do <strong>minimalismo</strong> na tatuagem. Usam agulhas muito finas para criar desenhos com <strong>linhas sutis</strong>, precisas e extremamente <strong>detalhadas</strong>. É perfeito para quem busca algo discreto, mas com <strong>alto nível de detalhe</strong>, como flores e escritas. A técnica foca na <strong>elegância</strong> e na <strong>limpeza</strong> do traço, muitas vezes em tinta preta, dando um ar de <strong>sofisticação</strong> à arte. É a prova de que menos é mais, né? 🤍",
        "image": "fineline-bg.jpg",
        "sub_styles": []
    },
    "geometric": {
        "title": "GEOMÉTRICO",
        "description": "Ah, geometria! Geralmente associada com a parte ruim da escola, no estilo geométrico ela dá fruto a formas incríveis! Seja através do uso do <strong>3D, pontilhismo ou blackwork</strong>, você vai ter uma tatuagem que desafia o relevo da pele humana. Com <strong>mandalas, formas não-euclidianas ou padrões repetitivos</strong>, o estilo geométrico é talvez aquele que melhor representa a criação do <strong>abstrato através de linhas exatas.</strong> É nesse estilo que se encontram aqueles que gostam <strong>ilusões de ótica, armaduras e a busca pelo nirvana.</strong> Ou talvez admirem o geométrico. De qualquer forma, namastê 🩶",
        "image": "geometric-bg.jpg",
        "sub_styles": []
    },
    "oldschool": {
        "title": "OLD SCHOOL",
        "description": "O <strong>retrô</strong> não morreu, ele continua firme e forte nos traços grossos do old school! Esse estilo vem reconquistando corações através de suas <strong>cores primárias fortes</strong> e <strong>contornos pretos.</strong> Com suas raízes na época da exploração marítima, o Old School é um estilo que <strong>representa força.</strong> Seja para homenagear o amor de mãe ou uma conquista que levou esforço, o Old School é o estilo perfeito para isso ❤️‍🩹",
        "image": "oldSchool-bg.jpg",
        "sub_styles": [
            {"name": "oriental", "title": "Oriental", "image": "oriental-bg.jpg"}
        ]
    },
    "oriental": {
        "title": "ORIENTAL",
        "description": "O estilo <strong>oriental</strong> passou por muitas mudanças ao longo do tempo. Inicialmente tendo traços e cores provindos de uma <strong>fusão do Old School com as antigas pinturas orientais</strong>, as tatuagens orientais são extremamente <strong>impactantes</strong> (para dizer o mínimo). Podemos ver o uso das <strong>cores primárias fortes</strong>, em combinação com <strong>grandes áreas escuras</strong>, formando um <strong>contraste</strong> palpável na pele. Esse estilo é bastante utilizado pela yakuza do japão, então tome cuidado ao viajar para lá. Apesar disso, é um estilo que <strong>exclama impacto</strong>, especialmente quando usado em áreas grandes como o tronco, braços e pernas. Ah droga, chega tô com vontade de fazer só mais um oni... 💜",
        "image": "oriental-bg.jpg",
        "sub_styles": []
    },
    "watercolor": {
        "title": "AQUARELA",
        "description": "A tatuagem em estilo <strong>Aquarela</strong> (ou<strong>Watercolor</strong>) é conhecida por sua <strong>vibratilidade</strong> e <strong>fluidez</strong>, imitando o efeito de uma pintura feita com pincel e água. Ela foge dos contornos pretos sólidos, priorizando<strong> manchas de cor translúcidas</strong>, respingos e o <strong>degradê suave</strong> entre os tons. O resultado é uma arte <strong>viva</strong> e <strong>etérea</strong>, que parece estar em movimento na pele. É muito usado para flores, animais e paisagens. A <strong>explosão de cor</strong> é o que mais chama a atenção 🧡",
        "image": "watercolor-bg.jpg",
        "sub_styles": []
    }
}

@main_bp.route("/styles/<style_name>")
def style_page(style_name):
    style_info = styles_data.get(style_name.lower())
    if not style_info:
        return "Estilo não encontrado", 404
    return render_template("style_template.html", style=style_info)