
let portia = {};
portia.puzzles = [];
portia.selected = null;
portia.answered = false;
portia.chosen = -1;

let display = {};
display.result = null;

function portiaICasketText(pointerArray) {
	let text = [];
	let p = 0;
	for (p in pointerArray) {
		text.push(textForPointer(parseInt(pointerArray[p]),parseInt(p)+1));
	}
	return text;
}

function portiaIRiddleText(truths) {
	let t = parseInt(truths);
	if (t === 0) {
		return "All statements on the caskets are false.";
	} if (t === 1) {
		return "There is only one true statement on the caskets.";
	}
	return "There are " + truths + " true statements on the caskets."
}

function htmlforCakets(pointerArray) {
	let html = "<table>";
	html += "<tr>"
	let txt = portiaICasketText(pointerArray);
	let i = 0;
	for (i in txt) {
		html += "<td> Casket " + (parseInt(i) + 1) + "</td>";
	}
	html += "</tr><tr>";
	for (i in txt) {
		html += "<td id='casket_" + (parseInt(i) + 1) + "' >" + openCasket() + "</td>";
	}
	html += "</tr><tr>";
	for (i in txt) {
		html += "<td>"+ txt[i] +"</td>"
	}
	html += "</tr><tr>";
	for (i in txt) {
		html += "<td>"+ htmlForButton(parseInt(i) + 1) + "</td>"
	}
	html += "</tr></table>";
	return html;
}

function htmlForButton(index) {
	html = "<button type='button' id='solve_"+ index +"' " ;
	html += " onclick='cellClick(event)'";
	html += " data-index='" + index + "'"
	html += " class='btn btn-secondary typeButton'>Select</span></button>";
	return html;
}

function cellClick(event) {
	if (portia.answered) return;
	let index = parseInt(event.target.getAttribute("data-index"));
	portia.chosen = index;
	let cell = document.getElementById( "casket_" + index);
	console.log("selected: " + cell);
	if (index === parseInt(portia.selected.solution)) {
		console.log("correct casket chosen");
		cell.innerHTML = "";
		cell.innerHTML = successCasket();
	} else {
		console.log("incorrect casket chosen");
		cellinnerHTML = "";
		cell.innerHTML = failCasket();
	}
	portia.answered = true;
	updateResult();
}


function updateResult(){
	if (portia.answered) {
		display.result.innerHTML = solutionText();
	} else {
		display.result.innerHTML = "";
	}
}

function solutionText() {
	if (portia.chosen === parseInt(portia.selected.solution)) {
		return "You chose wisely.";
	} else {
		return "You did not choose wisely.";
	}
}

function textForPointer(pointer, currentIndex) {
	let p = pointer;
	let negative = false;
	if (pointer < 0) {
		p = -1*pointer;
		negative = true;
	}
	if (p === currentIndex){
		if (negative){
			return "The portrait is not in this casket.";
		} else {
			return "The portrait is in this casket.";
		}
	}
	if (negative){
		return "The portrait is not in casket " + p +".";
	} else {
		return "The portrait is in casket " + p + ".";
	}
}

//-------------------------------------



/**
* Randomization Utilities
*/

function randomInt(lessThan){
	return Math.floor(Math.random()*lessThan);
};

/**
* returns a pseudo-random integer in the range 
* [greaterThan, lessThan]
*
*/
function randomRange(greaterThan, lessThan){
	var shifted = randomInt(lessThan - greaterThan + 1);
	return lessThan - shifted; 
};

function randomElement(array) {
	var res =randomRange(0, array.length-1);
	return array[res];
};

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;
  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = randomRange(0, currentIndex -1);
    currentIndex -= 1;
    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }
  return array;
};