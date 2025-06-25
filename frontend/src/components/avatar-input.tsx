"use client"

import { useRef, useState } from "react";
import { ControllerRenderProps, FieldPath, FieldValues } from "react-hook-form";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { UploadIcon, UserIcon } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@radix-ui/react-avatar";
import WebcamCapture, { ScreenshotData } from "@/components/webcam-capture";

interface AvatarInputProps<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
> {
  field: ControllerRenderProps<TFieldValues, TName>;
  label?: string;
}

export default function AvatarInput<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
>({ 
  field, 
  label = "Your Picture"
}: AvatarInputProps<TFieldValues, TName>) {
  const [avatarUrl, setAvatarUrl] = useState<string | undefined>(undefined);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Handle file selection
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setAvatarUrl(URL.createObjectURL(file));
      field.onChange(file);
    }
  };

  // Handle webcam capture
  const handleWebcamCapture = (data: ScreenshotData) => {
    setAvatarUrl(data.imageSrc);
    field.onChange(data.file);
  };

  // Handle upload button click
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <Popover>
        <PopoverTrigger asChild>
          <button
            type="button"
            className="w-24 h-24 rounded-full border-2 border-muted flex items-center justify-center overflow-hidden bg-muted hover:shadow-md transition-shadow focus:outline-none"
          >
            <Avatar>
              <AvatarImage
                src={avatarUrl}
                alt="Your avatar picture" 
              />
              <AvatarFallback>
                <UserIcon className="w-12 h-12 text-muted-foreground" />
              </AvatarFallback>
            </Avatar>
          </button>
        </PopoverTrigger>
        <PopoverContent className="w-48 flex flex-col gap-2">
          <WebcamCapture onCapture={handleWebcamCapture}/>
          <Button
            type="button"
            variant="ghost"
            className="justify-start gap-2"
            onClick={handleUploadClick}
          >
            <UploadIcon className="w-4 h-4" /> Upload Photo
          </Button>
        </PopoverContent>
      </Popover>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        className="hidden"
        onChange={handleFileChange}
        tabIndex={-1}
      />
      <span className="text-sm text-muted-foreground mt-1">{label}</span>
    </div>
  );
} 