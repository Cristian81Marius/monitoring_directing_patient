import {htmlFactory} from "./view/htmlFactory.js"
//import {dataHandler} from "./data/dataHandler"
import {domManager} from "./view/domManager.js"

function createCardHouse(){
    console.log("Houses")
    const build_card = htmlFactory.cardBuilder()
    domManager.addChild("#Houses", build_card)
}

createCardHouse()