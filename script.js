const colonne = 7;
const rangee = 6;
const sleep = ms => new Promise(r => setTimeout(r, ms));

function initialiser_board(colonne, rangee) {
    let board = document.querySelector("#board")
    board.innerHTML = ""
    for (let i = 0; i < rangee; i ++) {
        const tr = document.createElement("tr");
        const divTr = document.createElement("div");
        divTr.setAttribute('class', 'rangeBoard');
        tr.append(divTr);
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

}

function topJetons(colonne, couleur) {
    let topBoard = document.querySelector("#topBoard")
    topBoard.innerHTML = ""
    const tr = document.createElement("tr");
    const divTr = document.createElement("div");
    divTr.setAttribute('class', 'rangeBoard');
    tr.append(divTr);
    topBoard.append(tr);
    for (let i = 0; i < colonne; i++) {
        const td = document.createElement("td");
        const divTd = document.createElement("div");
        divTd.setAttribute('class', couleur)
        console.log(divTd.getAttribute('class'))
        td.append(divTd)
        tr.append(td);
    }
}

async function jouer(colonne, couleur) {
    for (let i = 0; i < rangee; i++) {
        let first = document.querySelector(`[name="${i}${colonne}"]`)
        if (first.getAttribute('class') === 'cercle') {
            first.setAttribute('class', couleur)
            await sleep(500);
            let next = document.querySelector(`[name="${i+1}${colonne}"]`)
            if (next != undefined){
                first.setAttribute('class', 'cercle')
            }
        }
    }
}

let boutonInit = document.querySelector("#boutonInit")
boutonInit.addEventListener("click", initialiser_board(colonne, rangee))


topJetons(7, "red")
jouer(5, 'red')
// jouer(5, 'yellow')
