import { useState, useRef, useCallback } from "react";
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
import { CameraIcon, VideoOffIcon } from "lucide-react";
import { toast } from "sonner";

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
  const [open, setOpen] = useState(false);
  const webcamRef = useRef<Webcam>(null);

  const showError = (e?: string | DOMException) => {
    toast.error("Oops! An error occured when taking your picture", {
      description: "Verify your browser permissions and check your media device",
    });
    e && console.error(e);
  }; 

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      
      if (imageSrc) {
        const file = dataUrlToFile(imageSrc);
        onCapture({ imageSrc, file });
        setOpen(false);
      } else {
        showError();
      }
    }
  }, [onCapture]);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button type="button" variant="ghost" className="justify-start gap-2">
          <CameraIcon className="w-4 h-4" /> Use Camera
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="sr-only"></DialogTitle>
        </DialogHeader>
        <div className="w-full flex justify-center">
          <div className="w-48 h-64 rounded-2xl overflow-hidden bg-gray-100 relative">
            {/* Background content */}
            <div className="absolute inset-0 flex items-center justify-center">
              <VideoOffIcon className="w-12 h-12 text-gray-400" />
            </div>
            
            {/* Foreground content */}
            <Webcam
              ref={webcamRef}
              audio={false}
              className="w-full h-full object-cover relative z-10"
              videoConstraints={{ 
                facingMode: "user",
                aspectRatio: 3/4,
              }}
              onUserMediaError={e => showError(e)}
            />
          </div>
        </div>
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
