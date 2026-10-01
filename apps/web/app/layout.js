import "./globals.css";

export const metadata = {
  title: "Practice",
  description: "CA practice workspace",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
