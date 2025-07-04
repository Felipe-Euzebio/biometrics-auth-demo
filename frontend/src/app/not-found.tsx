import Link from "next/link";
import { CircleAlert } from "lucide-react";
import NavigateBackButton from "@/components/navigate-back-button";

export default function NotFound() {
  return (
    <section className="bg-white dark:bg-gray-900 ">
      <div className="container flex items-center min-h-screen px-6 py-12 mx-auto">
        <div className="flex flex-col items-center max-w-sm mx-auto text-center">
          <p className="p-3 text-sm font-medium text-blue-500 rounded-full bg-blue-50 dark:bg-gray-800">
            <CircleAlert className="w-6 h-6" />
          </p>

          <h1 className="mt-3 text-2xl font-semibold text-gray-800 dark:text-white md:text-3xl">Oops!</h1>

          <p className="mt-4 text-gray-500 dark:text-gray-400">
            Looks like this page took a little detour!<br />
            Don't worry, we've got you covered:
          </p>

          <div className="flex items-center w-full mt-6 gap-x-3 shrink-0 sm:w-auto">
            <NavigateBackButton />
            <Link 
              href="/" 
              className="w-1/2 px-5 py-2 
                text-sm tracking-wide text-white 
                transition-colors duration-200 bg-blue-500 
                rounded-lg shrink-0 sm:w-auto 
                hover:bg-blue-600 dark:hover:bg-blue-500 dark:bg-blue-600 text-center"
            >
              Take me home
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}