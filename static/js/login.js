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

let config = {
	fps: 10,
	qrbox: 250,
	formatsToSupport: [Html5QrcodeSupportedFormats.QR_CODE, Html5QrcodeSupportedFormats.AZTEC],
	disableFlip: true,
}
let html5QrCode = new Html5Qrcode("camera", config)

async function start() {
	let cameras = await Html5Qrcode.getCameras()
	if (cameras && cameras.length > 0) {
		cameraCalledTest = true
	}
	html5QrCode.start(cameras[0].id, config, (decodedText, decodedResult) => {
		console.log(decodedText)
		fichar(decodedText)
	})
}

start()
