import { useRef, useCallback } from "react";
import Webcam from "react-webcam";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { CameraIcon } from "lucide-react";

// Convert DataURL to File
function dataUrlToFile(dataURL: string): File {
  const arr = dataURL.split(',');
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new File([u8arr], 'image.webp', { type: 'image/webp' });
}

export type ScreenshotData = {
  imageSrc: string;
  file: File;
};

interface WebcamCaptureProps {
  onCapture: (data: ScreenshotData) => void;
}

export default function WebcamCapture({ onCapture }: WebcamCaptureProps) {
  const webcamRef = useRef<Webcam>(null);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        const file = dataUrlToFile(imageSrc);
        onCapture({ imageSrc, file });
      }
    }
  }, [onCapture]);

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button type="button" variant="ghost" className="justify-start gap-2">
          <CameraIcon className="w-4 h-4" /> Use Camera
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="sr-only"></DialogTitle>
        </DialogHeader>
        <Webcam
          ref={webcamRef}
          audio={false}
          className="w-full h-full object-cover rounded-2xl"
          videoConstraints={{ facingMode: "user" }}
        />
        <DialogFooter className="sm:justify-center gap-2">
          <DialogClose asChild>
            <Button variant="outline" className="flex-1">Cancel</Button>
          </DialogClose>
          <Button onClick={capture} className="flex-1">
            Take Picture
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
