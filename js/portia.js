
function portiaICasketText(pointerArray) {
	let text = [];
	let p = 0;
	for (p in pointerArray) {
		text.push(textForPointer(parseInt(pointerArray[p]),parseInt(p)+1));
	}
	return text;
};

function portiaIRiddleText(truths) {
	let t = parseInt(truths);
	if (t === 0) {
		return "All statements on the caskets are false.";
	} if (t === 1) {
		return "There is only one true statement on the caskets.";
	}
	return "There are " + truths + " true statements on the caskets."
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