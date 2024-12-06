//==================================Speedometer========================================
class speedometer {
	constructor (maxSpeed, container1, container2) {
		// Set max speed to a multiple of 10
		while ((maxSpeed % 10) !== 0) {maxSpeed++;}
		// Get div containers
		this.scalesContainer = document.getElementById('scales-container');
		this.speedValues = document.getElementById('speed-values');
		this.container1 = document.getElementById(container1);
		this.container2 = document.getElementById(container2);
		this.speedDisplay = document.getElementById("value");
		this.arrow = document.getElementById("arrow-wrapper");
		// Build class variables 
		this.maxSpeed = maxSpeed + 10; //Add 10 to max speed for padding on the speedometer(optional)
		this.numScales = (this.maxSpeed / 5) + 1;
		this.speedPerAngle = this.maxSpeed / 230;
		this.angleGap = 5 / this.speedPerAngle;
		this.anglePerSpeed = 230 / this.maxSpeed
		this.currentRotation = -25
		// Initalize speedometer
		this.buildScales()
		this.resize()
	}

	resize() {
		const con1Width = this.container1.offsetWidth;
		
		this.container1.style.height = con1Width * 0.72 + "px"
		this.container2.style.height = con1Width * 0.72 + "px"
	}

	setSpeed(speed) {
		this.speedDisplay.innerHTML = speed;
		if (speed > this.maxSpeed) {speed = this.maxSpeed}
		let targetRotation = ((speed * this.anglePerSpeed) - 25)
		let direction = this.currentRotation < targetRotation ? "up" : "down"
		console.log( this.currentRotation + " < " + targetRotation + " : " + direction)
		if (this.currentRotation !== targetRotation) {
			let intervalId = setInterval(async () => {
				if (direction === "up"){
					//speed going up
					this.currentRotation += 0.5
					this.arrow.style.transform = "rotate("+ this.currentRotation + "deg)";
					if (this.currentRotation > targetRotation) {
						this.arrow.style.transform = "rotate("+ targetRotation + "deg)";
						clearInterval(intervalId)
					}
				} else {
					//speed going down
					this.currentRotation -= 0.5
					this.arrow.style.transform = "rotate("+ this.currentRotation + "deg)";
					if (this.currentRotation < targetRotation) {
						this.arrow.style.transform = "rotate("+ targetRotation + "deg)";
						clearInterval(intervalId)
					}
				}
			}, 10);
		}
	}
	// setSpeed(speed) {
	// 	this.speedDisplay.innerHTML = speed;
	// 	if (speed > this.maxSpeed) {speed = this.maxSpeed}
	// 	this.arrow.style.transform = "rotate("+ ((speed * this.anglePerSpeed) - 25) + "deg)";
	// }

	getRotationDegrees(obj) {
	  const matrix = window.getComputedStyle(obj).getPropertyValue('transform');

	  if (matrix !== 'none') {
	    const values = matrix.split('(')[1].split(')')[0].split(',');
	    const a = values[0];
	    const b = values[1];
	    const angle = Math.round(Math.atan2(b, a) * (180/Math.PI));

	    return angle;
	  }

	  return 0;
	}

	buildScales() {
		var htmlString = "";
		var htmlString2 = "";
		for (let i=0; i < this.numScales; i++) {
			if (((i % 2) === 1) && (this.numScales > 15)) {
				htmlString = htmlString + "<div class='half-scale-container scale-" + i + "' style='transform: rotate(" +((this.angleGap * i) - 115)+ "deg);'><div class='scales'></div></div>"
			}
			else {
				
				htmlString = htmlString + "<div class='scale-container scale-" + i + "' style='transform: rotate(" +((this.angleGap * i) - 115)+ "deg);'><div class='scales'></div></div>"
				htmlString2 = htmlString2 + "<div class='scale-values speed-scale-" + i + "' style='transform: rotate(" +((this.angleGap * i) - 115)+ "deg);'><div class='speed-scale-value-top' style=' transform: rotate("+ -((this.angleGap * i) - 115) +"deg);'>"+ (5 * i) +"</div></div>"
			}
		}

		this.scalesContainer.innerHTML = htmlString
		this.speedValues.innerHTML = htmlString2
	}
}

//==================================Steering Graphic========================================
function setAngle(angle) {
	document.getElementById("steering-angle").innerHTML = angle +"°"
	document.getElementById("left-wheel").style.transform = "rotate("+ (angle) + "deg)"
	document.getElementById("right-wheel").style.transform = "rotate("+ (angle) + "deg)"
}
