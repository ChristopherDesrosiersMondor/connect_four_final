const colonne = 7;
const rangee = 6;
const couleur1 = 'red';
const couleur2 = 'yellow';
var nbTours = 0;
const sleep = ms => new Promise(r => setTimeout(r, ms));
var matrice_jeu = []
const message = document.querySelector(".message")
let async_running = false

// Source: pluralsight.com/guides/work-with-ajax-django
// Utilisation: envoyer des requetes a d'autres views a partir de js avec jquery et ajax

function initialiser_board() {
    if (async_running){
        await
    }
    nbTours = 1;
    const board = document.querySelector("#board")
    board.setAttribute('style', 'visibility: visible')
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
    let couleur = couleur2
    topJetons(couleur)
}

function topJetons(couleur) {
    const topBoard = document.querySelector("#topBoard")
    topBoard.setAttribute('style', 'visibility: visible')
    topBoard.setAttribute('class', 'topBoard')
    topBoard.innerHTML = ""
    const tr = document.createElement("tr");
    tr.setAttribute('class', 'rangeBoard');
    topBoard.append(tr);
    for (let i = 0; i < colonne; i++) {
        const td = document.createElement("td");
        const boutonJeton = document.createElement("button");
        boutonJeton.setAttribute('class', `${couleur} topBouton`);
        boutonJeton.setAttribute('id', `btn${i}`);
        td.append(boutonJeton);
        tr.append(td);
    }
    if (couleur === 'yellow') {
        message.innerHTML = "> c'est ton tour!"
        let boutons = document.querySelectorAll(".topBouton")

        for (let i = 0; i < boutons.length; i++) {
            boutons[i].addEventListener("click", function(){jouer(i, couleur)}, false)
        }
    }
    else {
        message.innerHTML = "> c'est le tour de <br/> > l'ordinateur"
    }
}

async function tour() {
    nbTours += 1;
    var couleur = null
    if (nbTours % 2 === 0) {
        async_running = true
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
            success : async function(response) {
                console.log(response)
                let colonne = response.col
                await jouer(colonne - 1, couleur)
                if (response.win){
                    message.innerHTML = "> l'ordinateur a gagné!"
                    board.setAttribute('style', 'visibility: hidden')
                    topBoard.setAttribute('style', 'visibility: hidden')
                }
            }
        })
    }
    else {
        async_running = false
        couleur = couleur2;
        topJetons(couleur)
    }
}


async function jouer(colonne, couleur) {
    let topBoutons = document.querySelector('.rangeBoard')
    topBoutons.style.visibility = 'hidden'

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
    let full = edit_matrice()

    if (full) {
        message.innerHTML = "> la partie est nulle"
        board.setAttribute('style', 'visibility: hidden')
        topBoard.setAttribute('style', 'visibility: hidden')
    }

    if (couleur === couleur2) {
        $.ajax({
            url: "jouer_adv/",
            data : {
                matrice: JSON.stringify(matrice_jeu)
            },
            success : async function(response) {
                if (response.win){
                    message.innerHTML = '> vous avez gagné!'
                    board.setAttribute('style', 'visibility: hidden')
                    topBoard.setAttribute('style', 'visibility: hidden')
                }
            }
        })
    }
    await
    tour()
    console.log("button clicked");
}



function edit_matrice() {
    let board = document.querySelector("#board");
    let rangees = board.querySelectorAll("tr");
    let caseVide = 0;
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
                caseVide += 1;
            }
        }
    }
    if (caseVide === 0) {
        return true;
    }

}


let boutonInit = document.querySelector("#boutonInit");
boutonInit.addEventListener("click", function(){initialiser_board(colonne, rangee, 'yellow')}, false);





