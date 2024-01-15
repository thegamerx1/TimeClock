function clock() {
	let date = new Date()
	$("#clocky").text(
		`${date.getFullYear()}/${padNumber(date.getMonth() + 1)}/${padNumber(
			date.getDate()
		)} ${padNumber(date.getHours())}:${padNumber(date.getMinutes())}:${padNumber(
			date.getSeconds()
		)}.${padNumber(date.getMilliseconds())}`
	)
	requestAnimationFrame(clock)
}

function padNumber(num) {
	return num.toString().padStart(2, "0")
}

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
	await sleep(2000)
	$(".close-modalDenegado")[0].click()
	makingRequest = false
}

async function Permitido(mensaje, id_voz) {
	$("#mensajepermitido").text(mensaje)
	$("#boton-modalPermitido").click()
	playAudio(id_voz)
	await sleep(3500)
	$(".close-modalPermitido")[0].click()
	makingRequest = false
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

let html5QrcodeScanner = new Html5Qrcode("reader")
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

async function start() {
	let camaras = await Html5Qrcode.getCameras()
	console.log(camaras)
	let camara = camaras[0]
	html5QrcodeScanner.start(camara.id, { fps: 30 }, (decodedText, decodedResult) => {
		fichar(decodedText)
	})
}

start()
