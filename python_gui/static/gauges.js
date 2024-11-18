//==================================Speedometer========================================
function resize (container1, container2) {
		const con1 = document.getElementById(container1);
		const con2 = document.getElementById(container2);
		const con1Width = con1.offsetWidth;
		
		con1.style.height = con1Width * 0.72 + "px"
		con2.style.height = con1Width * 0.72 + "px"
	}

function setSpeed (maxSpeed, speed){
	while ((maxSpeed % 5) !== 0) {maxSpeed++;}

	maxSpeed = maxSpeed + 10;
	anglePerSpeed = 230 / maxSpeed

	document.getElementById("value").innerHTML = speed;
	if (speed > maxSpeed) {speed = maxSpeed}
	document.getElementById("arrow-wrapper").style.transform = "rotate("+ ((speed * anglePerSpeed) - 25) + "deg)";
}

function initalizeSpeedometer(maxSpeed, container1, container2) {

	resize('speedometer-container-1', 'speedometer-container-2')

	while ((maxSpeed % 5) !== 0) {maxSpeed++;}

	scalesContainer = document.getElementById('scales-container')
	speedValues = document.getElementById('speed-values')
	maxSpeed = maxSpeed + 10;
	numScales = (maxSpeed / 5) + 1;
	speedPerAngle = maxSpeed / 230;
	angleGap = 5 / speedPerAngle;
	htmlString = "";
	htmlString2 = "";

	for (i=0; i < numScales; i++) {
		if (((i % 2) === 1) && (numScales > 15)) {
			htmlString = htmlString + "<div class='half-scale-container scale-" + i + "' style='transform: rotate(" +((angleGap * i) - 115)+ "deg);'><div class='scales'></div></div>"
		}
		else {
			
			htmlString = htmlString + "<div class='scale-container scale-" + i + "' style='transform: rotate(" +((angleGap * i) - 115)+ "deg);'><div class='scales'></div></div>"
			htmlString2 = htmlString2 + "<div class='scale-values speed-scale-" + i + "' style='transform: rotate(" +((angleGap * i) - 115)+ "deg);'><div class='speed-scale-value-top' style=' transform: rotate("+ -((angleGap * i) - 115) +"deg);'>"+ (5 * i) +"</div></div>"
		}
	}

	scalesContainer.innerHTML = htmlString
	speedValues.innerHTML = htmlString2

}

// function initalizeSpeedometer(numScales, container1, container2) {

// 	resize('speedometer-container-1', 'speedometer-container-2')

// 	scalesContainer = document.getElementById('scales-container')
// 	speedValues = document.getElementById('speed-values')
// 	htmlString = ""
// 	htmlString2 = ""
// 	angleGap = (180/numScales)
// 	speedsListtemp = []
// 	speedsList = []

// 	for (i=0; i < numScales; i++){speedsListtemp.push(((180/numScales)*i)); speedsListtemp.push(((180/numScales)*i)-180);}
// 	for (i=0; i < speedsListtemp.length; i++){if (speedsListtemp[i] > -110 && speedsListtemp[i] < 110){speedsList.push(speedsListtemp[i])}}
	
// 	speedsList.sort(function (a, b) { return a - b })
// 	speedScale = 56 / 230

// 	for (i=0; i < numScales; i++) {
// 		htmlString = htmlString + "<div class='scales scale-" + i + "' style='transform: rotate(" +((180/numScales)*i)+ "deg);'></div>"

// 		if ((((180/numScales)*i) < 115) && !((((180/numScales)*i)-180) > -110)){
// 			htmlString2 = htmlString2 + "<div class='scale-values speed-scale-" + i + "' style='transform: rotate(" +((180/numScales)*i)+ "deg);'><div class='speed-scale-value-top' style=' transform: rotate("+ -((180/numScales)*i) +"deg);'>"+ Math.round(((speedsList.indexOf(((180/numScales))*i)*speedScale)*angleGap)) +"</div></div>"
// 		}
// 		if (((((180/numScales)*i)-180) > -110) && (((180/numScales)*i) < 115)) {
// 			htmlString2 = htmlString2 + "<div class='scale-values speed-scale-" + i + "' style='transform: rotate(" +((180/numScales)*i)+ "deg);'><div class='speed-scale-value-top' style=' transform: rotate("+ -((180/numScales)*i) +"deg);'>"+ Math.round(((speedsList.indexOf(((180/numScales))*i)*speedScale)*angleGap)) +"</div><div class='speed-scale-value-bottom' style='transform: rotate("+ -((180/numScales)*i) +"deg);'>"+ Math.round(((speedsList.indexOf(((180/numScales)*i)-180)*speedScale)*angleGap)) +"</div></div>"
// 		}

// 		if ((((180/numScales)*i) > 115)) {
// 			htmlString2 = htmlString2 + "<div class='scale-values speed-scale-" + i + "' style='transform: rotate(" +((180/numScales)*i)+ "deg);'><div class='speed-scale-value-bottom' style='transform: rotate("+ -((180/numScales)*i) +"deg);'>"+ Math.round(((speedsList.indexOf(((180/numScales)*i)-180)*speedScale)*angleGap)) +"</div></div>"
// 		}

// 	}

// 	scalesContainer.innerHTML = htmlString
// 	speedValues.innerHTML = htmlString2
// }

function handleResize() {console.log("Window resized!"); }

window.addEventListener("resize", function(){resize('speedometer-container-1', 'speedometer-container-2')});

//==================================Steering Graphic========================================
function setAngle(angle) {
	document.getElementById("steering-angle").innerHTML = angle +"°"
	document.getElementById("left-wheel").style.transform = "rotate("+ (angle) + "deg)"
	document.getElementById("right-wheel").style.transform = "rotate("+ (angle) + "deg)"
}
