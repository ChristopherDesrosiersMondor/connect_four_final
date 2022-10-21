const colonne = 7;
const rangee = 6;
const couleur1 = 'red';
const couleur2 = 'yellow';
var nbTours = NaN;
const sleep = ms => new Promise(r => setTimeout(r, ms));

function initialiser_board() {
    var nbTours = 0;
    let board = document.querySelector("#board")
    board.innerHTML = ""
    board.setAttribute('class', 'board')
    for (let i = 0; i < rangee; i ++) {
        const tr = document.createElement("tr");
        tr.setAttribute('class', 'rangeBoard');
        board.append(tr);
        for (let j = 0; j < colonne; j++) {
            const td = document.createElement("td");
            const divTd = document.createElement("div");
            divTd.setAttribute('class', 'cercle');
            divTd.setAttribute('name', `${i}${j}`);
            td.append(divTd);
            tr.append(td);
        }
    }
    // game();
    tour();
}

function topJetons(couleur) {
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
        td.append(boutonJeton);
        tr.append(td);
    }
}

function tour() {
    nbTours += 1;
    if (nbTours % 2 === 1) {
        var couleur = couleur1;
    }
    else {
        var couleur = couleur2;
    }
    topJetons(couleur)
    let btn0 = document.querySelector('#btn0');
    let btn1 = document.querySelector('#btn1');
    let btn2 = document.querySelector('#btn2');
    let btn3 = document.querySelector('#btn3');
    let btn4 = document.querySelector('#btn4');
    let btn5 = document.querySelector('#btn5');
    let btn6 = document.querySelector('#btn6');
    
    btn0.addEventListener("click", function(){jouer(0, couleur)}, false);
    btn1.addEventListener("click", function(){jouer(1, couleur)}, false);
    btn2.addEventListener("click", function(){jouer(2, couleur)}, false);
    btn3.addEventListener("click", function(){jouer(3, couleur)}, false);
    btn4.addEventListener("click", function(){jouer(4, couleur)}, false);
    btn5.addEventListener("click", function(){jouer(5, couleur)}, false);
    btn6.addEventListener("click", function(){jouer(6, couleur)}, false);}


async function jouer(colonne, couleur) {
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
    tour();
}

function game() {
    for (i = 0; i < 10; i++) {
        tour()
    }
}

let boutonInit = document.querySelector("#boutonInit");
boutonInit.addEventListener("click", function(){initialiser_board(colonne, rangee, 'yellow')}, false);






