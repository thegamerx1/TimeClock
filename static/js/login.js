function clock() {
	let date = new Date()
	$("#clocky").text(
		`${date.getFullYear()}/${padNumber(date.getMonth() + 1)}/${padNumber(
			date.getDate()
		)} ${padNumber(date.getHours())}:${padNumber(date.getMinutes())}:${padNumber(
			date.getSeconds()
		)}`
	)
	requestAnimationFrame(clock)
}

const SLEEPTIME = 2500

function padNumber(num) {
	return num.toString().padStart(2, "0")
}

//  If the test fails it means the camera hasn't been initialized for 5 seconds so we reload hoping it works the next time
let cameraCalledTest = false

setTimeout(() => {
	if (!cameraCalledTest) {
		window.location.reload()
	}
}, 5000)

requestAnimationFrame(clock)

let makingRequest = false
function fichar(idCodigoQr) {
	if (makingRequest) return
	makingRequest = true
	$.ajax("/loginCodigoQR", {
		data: {
			pinCodigoQR: idCodigoQr,
		},
		dataType: "json",
		success: function (data) {
			if (data.success) {
				Permitido(data.mensaje, data.voz_id)
			} else {
				Denegado()
			}
			setTimeout(() => {
				makingRequest = false
			}, SLEEPTIME)
		},
		type: "POST",
	})
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms))
}

function playAudio(id_voz) {
	var audio = new Audio("/voz/" + id_voz)
	audio.play()
}

async function Denegado() {
	$("#boton-modalDenegado").click()
	await sleep(SLEEPTIME)
	$(".close-modalDenegado")[0].click()
}

async function Permitido(mensaje, id_voz) {
	$("#mensajepermitido").text(mensaje)
	$("#boton-modalPermitido").click()
	playAudio(id_voz)
	await sleep(SLEEPTIME)
	$(".close-modalPermitido")[0].click()
}

$("#boton-modalDenegado").animatedModal({
	animatedIn: "bounceIn",
	animatedOut: "bounceOut",
	animationDuration: ".2s",
	color: "rgba(0,0,0,0)",
})
$("#boton-modalPermitido").animatedModal({
	animatedIn: "bounceIn",
	animatedOut: "bounceOut",
	animationDuration: ".2s",
	color: "rgba(0,0,0,0)",
})

window.addEventListener("load", function () {
	let codeReader = new ZXing.BrowserMultiFormatReader()
	let video = document.querySelector("#camera > video")
	console.log("ZXing code reader initialized")
	codeReader.listVideoInputDevices().then(videoInputDevices => {
		let selectedDeviceId = videoInputDevices[0].deviceId

		codeReader.decodeFromVideoDevice(selectedDeviceId, video, (result, err) => {
			cameraCalledTest = true
			if (result) {
				fichar(result.text)
			}
			if (err && !(err instanceof ZXing.NotFoundException)) {
				console.error(err)
			}
		})
		console.log(`Started continous decode from camera with id ${selectedDeviceId}`)
	})
})

// async function start() {
// 	let camaras = await Html5Qrcode.getCameras()
// 	console.log(camaras)
// 	let camara = camaras[0]
// 	html5QrcodeScanner.start(camara.id, { fps: 30 }, (decodedText, decodedResult) => {
// 		fichar(decodedText)
// 	})
// }

// start()
// let html5QrcodeScanner = new Html5Qrcode("reader")
// $("#login-form").on("submit", e => {
// 	e.preventDefault()
// 	$.ajax("/login", {
// 		data: {
// 			pin: $("#pin").val(),
// 			userId: $("#persona").val(),
// 		},
// 		dataType: "json",
// 		success: function (data) {
// 			if (data.success) {
// 				Permitido(data.mensaje)
// 			} else {
// 				Denegado()
// 			}
// 		},
// 		type: "POST",
// 	})
// })
