import FilmesEmAlta from "@/components/features/home/FilmesEmAlta";
import SeriesEmAlta from "@/components/features/home/SeriesEmAlta";
import Header from "@/components/ui/Header";

export default async function HomePage() {
  return (
    <>
      <Header />
      <main className="py-8 max-w-375 mx-auto w-full px-5 2xl:px-0">
        <FilmesEmAlta />
        <SeriesEmAlta />
      </main>
    </>
  );
}
