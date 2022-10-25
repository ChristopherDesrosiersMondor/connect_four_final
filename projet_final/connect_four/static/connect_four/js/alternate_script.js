const colonne = 7;
const rangee = 6;
const couleur1 = 'red';
const couleur2 = 'yellow';
var nbTours = 0;
const sleep = ms => new Promise(r => setTimeout(r, ms));
var matrice_jeu = []
let list_bouton = []

// Source: pluralsight.com/guides/work-with-ajax-django
// Utilisation: envoyer des requetes a d'autres views a partir de js avec jquery et ajax

function initialiser_board() {
    var nbTours = 0;
    let board = document.querySelector("#board")
    board.innerHTML = ""
    board.setAttribute('class', 'board')
    for (let i = 0; i < rangee; i ++) {
        const tr = document.createElement("tr");
        tr.setAttribute('class', 'rangeBoard');
        board.append(tr);
        matrice_jeu[i] = []
        for (let j = 0; j < colonne; j++) {
            const td = document.createElement("td");
            const divTd = document.createElement("div");
            divTd.setAttribute('class', 'cercle');
            divTd.setAttribute('name', `${i}${j}`);
            td.append(divTd);
            tr.append(td);
            matrice_jeu[i][j] = ''
        }
    }
    // game();
    tour();
}

function topJetons(couleur) {
    list_bouton = []
    let topBoard = document.querySelector("#topBoard")
    topBoard.setAttribute('class', 'topBoard')
    topBoard.innerHTML = ""
    const tr = document.createElement("tr");
    const divTr = document.createElement("div");
    divTr.setAttribute('class', 'rangeBoard');
    tr.append(divTr);
    topBoard.append(tr);
    for (let i = 0; i < colonne; i++) {
        const td = document.createElement("td");
        const boutonJeton = document.createElement("button");
        boutonJeton.setAttribute('class', couleur);
        boutonJeton.setAttribute('id', `btn${i}`);
        boutonJeton.col = i
        boutonJeton.couleur = couleur
        td.append(boutonJeton);
        tr.append(td);
        list_bouton.push(boutonJeton)
    }
}

async function tour() {
    nbTours += 1;
    var couleur = null
    if (nbTours % 2 === 0) {
        couleur = couleur1;
        topJetons(couleur)
        var isAI = false
        if (couleur === 'red') {
            isAI = true
        }
        console.log("data: " + JSON.stringify(matrice_jeu));
        $.ajax({
            url: "jouer/",
            data : {
                matrice: JSON.stringify(matrice_jeu)
            },
            success : function(response) {
                console.log(response)
                jouer_ai(response - 1, couleur)
            }
        })
    }
    else {
        couleur = couleur2;
        topJetons(couleur)

        for (let i = 0; i < list_bouton.length ; i++) {
            list_bouton[i].addEventListener("click", jouer, false)
        }
    }
}


async function animation(colonne, couleur) {
    for (let i = 0; i < rangee; i++) {
        let first = document.querySelector(`[name="${i}${colonne}"]`)
        if (first.getAttribute('class') === 'cercle') {
            first.setAttribute('class', couleur)
            await sleep(500);
            let next = document.querySelector(`[name="${i+1}${colonne}"]`)
            if (next != undefined && next.getAttribute('class') === 'cercle'){
                first.setAttribute('class', 'cercle')
            }
        }
    }
}

function update_state() {
    edit_matrice()
    tour();
    console.log("button clicked");
}

async function jouer_ai(colonne, couleur) {
    let topBoutons = document.querySelector('.rangeBoard')
    topBoutons.style.visibility = 'hidden'
    animation(colonne, couleur)
    update_state()
}

async function jouer(event) {
    let topBoutons = document.querySelector('.rangeBoard')
    topBoutons.style.visibility = 'hidden'

    let couleur = event.currentTarget.couleur
    let colonne = event.currentTarget.col
    animation(colonne, couleur)
    update_state()
}


function edit_matrice() {
    let board = document.querySelector("#board");
    let rangees = board.querySelectorAll("tr");
    for (let i = 0; i < rangees.length; i++) {
        let colonnes = rangees[i].querySelectorAll('td')
        for (let j = 0; j < colonnes.length; j++) {
            classe = colonnes[j].children[0].getAttribute('class')
            if (classe === 'yellow') {
                matrice_jeu[i][j] = 'Y'
            }
            else if (classe === 'red') {
                matrice_jeu[i][j] = 'R'
            }
            else {
                matrice_jeu[i][j] = ''
            }
        }
    }
    console.log(matrice_jeu)
}

function game() {
    for (i = 0; i < 10; i++) {
        tour()
    }
}

let boutonInit = document.querySelector("#boutonInit");
boutonInit.addEventListener("click", function(){initialiser_board(colonne, rangee, 'yellow')}, false);






