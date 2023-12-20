let html5QrcodeScanner = new Html5Qrcode("reader")

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

async function Permitido(username, id_voz) {
	$("#nombre").html(username)
	$("#boton-modalPermitido").click()
	playAudio(id_voz)
	await sleep(2000)
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

// Permitido("juan")

$("#login-form").on("submit", e => {
	e.preventDefault()
	$.ajax("/login", {
		data: {
			pin: $("#pin").val(),
			userId: $("#persona").val(),
			piso: PISO,
		},
		dataType: "json",
		success: function (data) {
			if (data.success) {
				Permitido()
			} else {
				Denegado()
			}
		},
		type: "POST",
	})
})

let makingRequest = false
async function start() {
	let camaras = await Html5Qrcode.getCameras()
	console.log(camaras)
	let camara = camaras[0]
	html5QrcodeScanner.start(camara.id, { fps: 5 }, (decodedText, decodedResult) => {
		if (makingRequest) return
		makingRequest = true
		$.ajax("/loginCodigoQR", {
			data: {
				pinCodigoQR: decodedText,
			},
			dataType: "json",
			success: function (data) {
				if (data.success) {
					Permitido(data.username, data.voz_id)
				} else {
					Denegado()
				}
			},
			type: "POST",
		})
	})
}

start()
