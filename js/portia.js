
let portia = {};
portia.puzzles = [];
portia.selected = null;
portia.answered = false;
portia.chosen = -1;
portia.version = 1;

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

function textForVersion() {
	let text = "";
	if (portia.version === 1) {
		text = "Portia I invites the user to choose the casket concealing the "
		text += "portrait based on knowing the overall number of true statements on the caskets."
	} else if (portia.version === 2) {
		text = "The caskets from Portia II have two inscriptions instead of just one. "
		text += "Casket selection is based on knowing the distribution of true statements among the caskets.";
	} else {
		text = "Portia III introduces the casket makers Bellini and Cellini. Bellini’s inscriptions are always "
		text += "true, and Cellini’s are always false. Once you determine which caskets were made by whom, the "
		text += "inscriptions will lead the way to the portrait."
	}
	return text;
}

function portiaIRiddleText(p) {
	let truths = p.truths
	if (portia.version == 1) {
		let t = parseInt(truths);
		if (t === 0) return "All statements on the caskets are false.";
		if (t === 3) return "All statements on the caskets are true.";
		
		if (p.position === "max") return "There are at least " + truths + " true statements on the caskets.";
		if (p.position === "min") return "There are at most " + truths + " true statements on the caskets.";
		if (t === 1) return "Of all the statments on the caskets, only one is true.";		
		return "There are " + truths + " true statements on the caskets."
	} else if (portia.version == 2) {
		text = "";
		let zeroCount = 0;
		let oneCount = 0;
		let twoCount = 0;
		for (i in truths){
			let ic = parseInt(truths[i])
			if (ic === 0) {
				zeroCount ++;
			} else if (ic === 1){
				oneCount ++;			
			} else if (ic === 2){
				twoCount ++;
			}
		}
		if (zeroCount == 1){
			text += "There is one casket with a no true statements. ";
		} else if (zeroCount != 0) {
			text += "There are " + zeroCount + " caskets with no true statements. "
		} 
		if (oneCount == 1) {
			text += "There is one casket with one true statement. "
		} else if (oneCount != 0) {
			text += "There are " + oneCount + " caskets with one true statement. "
		}
		if (twoCount == 1) {
			text += "There is one casket with two true statements."
		} else if (twoCount != 0) {
			text += "There are " + twoCount + " caskets with two true statements. "			
		}
		return text;
	} else if (portia.version == 3) {
		return "Caskets made by Bellini have true inscriptions, <br> caskets made by Cellini have false inscriptions."
	}
}

function htmlforCakets(p) {
	let pointerArray = p.caskets;
	let html = "<table>";
	html += "<tr>"
	let txt = [];
	if (portia.version == 1) {
		txt = portiaICasketText(pointerArray);
	} else if (portia.version == 2){
		let txt1 = portiaICasketText(pointerArray[0]);
		let txt2 = portiaICasketText(pointerArray[1]);
		let x = 0;
		for (x in txt1){
			txt.push(txt1[x] + "<br>" + txt2[x])
		}
	} else if (portia.version == 3){
		let txt1 = portiaICasketText(pointerArray[0]);
		let txt2 = belliniCelliniCasket(pointerArray[1], p.truths);
		for (x in txt1){
			txt.push(txt1[x] + "<br>" + txt2[x])
		}
	}
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

function belliniCelliniCasket(pointers, truths) {
	let results = [];
	let i = 0;
	for (i in pointers) {
		let target = pointers[i];
		let isSympathy = false;
		if (target < 0){
			isSympathy = true;
			target = -1*target;
		}
		let sourceT = truths[i];
		let targetT = truths[target-1];
		let text = "";
		if (isSympathy){
			if (targetT===1) {
				text = "Fashioned by the same maker as " + target + ".";
			} else {
				text = "Fashioned by a different maker than " + target +".";
			}
		} else {
			if (sourceT === targetT) {
				text = "Casket " + target + " is made by Bellini.";	
			} else {
				text = "Casket " + target + " is made by Cellini.";
			}
		}
		results.push(text);
	}
	return results;
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
	let close = " The portrait was in casket " + portia.selected.solution +".";
	if (portia.chosen === parseInt(portia.selected.solution)) {
		return "You chose wisely." + close;
	} else {
		return "You did not choose wisely." + close;
	}
}

function textForPointer(pointer, currentIndex) {
	let selfNegative = ["The portrait is not in this casket.", "The portrait is not in here.","This casket is empty."];
	let selfPositive = ["The portrait is in this casket.", "The portrait is in here.","This casket has the portriat."]
	let p = pointer;
	let negative = false;
	if (pointer < 0) {
		p = -1*pointer;
		negative = true;
	}
	if (p === currentIndex){
		if (negative){
			return randomElement(selfNegative);
		} else {
			return randomElement(selfPositive);
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