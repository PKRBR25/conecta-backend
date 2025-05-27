import Image from "next/image";
import { Metadata } from "next";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "SaaS Login",
  description: "Secure login system for corporate employees",
};

export default function Home() {
  // Redirect to login page by default
  redirect("/login");
  
  return null; // This line is needed for TypeScript, though redirect will prevent it from being reached
}
