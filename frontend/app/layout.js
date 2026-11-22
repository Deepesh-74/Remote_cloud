export const metadata = {
  title: "AI Media Forensics",
  description: "Baseline image forensics dashboard"
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
