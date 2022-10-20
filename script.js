function initialiser_board(colonne, rangee) {
    let board = document.querySelector("#board")
    board.innerHTML = ""
    for (let i = 0; i < rangee; i ++ ) {
        const tr = document.createElement("tr");
        const divTr = document.createElement("div")
        divTr.setAttribute('class', 'rangeBoard')
        tr.append(divTr)
        board.append(tr);
        for (let j = 0; j < colonne; j++) {
            const td = document.createElement("td");
            const divTd = document.createElement("div");
            divTd.setAttribute('class', 'cercle')
            td.append(divTd)
            tr.append(td);
        }
    }

}

let boutonInit = document.querySelector("#boutonInit")
boutonInit.addEventListener("click", initialiser_board(7,6))
