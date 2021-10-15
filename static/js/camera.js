// const medias = {
//     audio : false,
//     video : true
//   };
// const video = document.getElementById("video");
// const promise = navigator.mediaDevices.getUserMedia(medias);

// promise.then(successCallback)
//     .then(errorCallback);

// function successCallback(stream) {
//     video.srcObject = stream;
// };

// function errorCallback(err) {
//     alert(err);
// };

var _scannerIsRunning = false;

function startScanner() {
  Quagga.init(
    {
      inputStream: {
        name: "Live",
        type: "LiveStream",
        target: document.querySelector("#scanner-container"),
        constraints: {
          width: 480,
          height: 320,
          facingMode: "environment",
        },
      },
      decoder: {
        readers: [
          "code_128_reader",
          "ean_reader",
          "ean_8_reader",
          "code_39_reader",
          "code_39_vin_reader",
          "codabar_reader",
          "upc_reader",
          "upc_e_reader",
          "i2of5_reader",
        ],
        debug: {
          showCanvas: true,
          showPatches: true,
          showFoundPatches: true,
          showSkeleton: true,
          showLabels: true,
          showPatchLabels: true,
          showRemainingPatchLabels: true,
          boxFromPatches: {
            showTransformed: true,
            showTransformedBox: true,
            showBB: true,
          },
        },
      },
    },
    function (err) {
      if (err) {
        console.log(err);
        return;
      }

      console.log("Initialization finished. Ready to start");
      Quagga.start();

      // Set flag to is running
      _scannerIsRunning = true;
    }
  );

  Quagga.onProcessed(function (result) {
    var drawingCtx = Quagga.canvas.ctx.overlay,
      drawingCanvas = Quagga.canvas.dom.overlay;

    if (result) {
      if (result.boxes) {
        drawingCtx.clearRect(
          0,
          0,
          parseInt(drawingCanvas.getAttribute("width")),
          parseInt(drawingCanvas.getAttribute("height"))
        );
        result.boxes
          .filter(function (box) {
            return box !== result.box;
          })
          .forEach(function (box) {
            Quagga.ImageDebug.drawPath(box, { x: 0, y: 1 }, drawingCtx, {
              color: "green",
              lineWidth: 2,
            });
          });
      }

      if (result.box) {
        Quagga.ImageDebug.drawPath(result.box, { x: 0, y: 1 }, drawingCtx, {
          color: "#00F",
          lineWidth: 2,
        });
      }

      if (result.codeResult && result.codeResult.code) {
        Quagga.ImageDebug.drawPath(
          result.line,
          { x: "x", y: "y" },
          drawingCtx,
          { color: "red", lineWidth: 3 }
        );
      }
    }
  });

  Quagga.onDetected(function (result) {
    let ISBN = result.codeResult.code;
    if (ISBN.length === 13 && ISBN.slice(0,3)==="978") {
      console.log("ISBN detected and processed : [" + ISBN + "]", result);
      Quagga.stop();
    }
  });
}

// Start/stop scanner
document.getElementById("btn").addEventListener(
  "click",
  function () {
    if (_scannerIsRunning) {
      Quagga.stop();
    } else {
      startScanner();
    }
  },
  false
);
