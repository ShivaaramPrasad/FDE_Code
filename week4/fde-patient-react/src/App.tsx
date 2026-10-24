import Header from './components/Header';
import PatientTable from './components/PatientTable';
import type { Encounter } from './assets/types';
import { usePaginatedFetch } from './hooks/usePaginatedFetch';
import Pagination from './components/Pagination';
import './App.css'

const FETCH_LIMIT = 500;
const PAGE_SIZE = 20;

function App() {
  const { pageData: pageEncounters, loading, error, page, totalPages, setPage } =
    usePaginatedFetch<Encounter>("http://localhost:8000/encounters", FETCH_LIMIT, PAGE_SIZE);

  return (
    <div>
      <Header />
      {loading && <p>Loading encounters...</p>}
      {error && <p>Error: {error}</p>}
      {!loading && !error && (
        <>
          <PatientTable encounters={pageEncounters} />
          <Pagination currentPage={page} totalPages={totalPages} onPageChange={setPage} />
        </>
      )}
    </div>
  );
}

export default App;
