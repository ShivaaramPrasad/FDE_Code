import Header from './components/Header';
import PatientTable from './components/PatientTable';
import { useState } from "react";
import type { Encounter } from './assets/types';
import { usePaginatedFetch } from './hooks/usePaginatedFetch';
import Pagination from './components/Pagination';
import './App.css'

const FETCH_LIMIT = 500;
const PAGE_SIZE = 20;

function App() {
  const { data: encounters, loading, error } = usePaginatedFetch<Encounter>("http://localhost:8000/encounters", FETCH_LIMIT);
  const [page, setPage] = useState(1);

  const totalPages = Math.max(1, Math.ceil(encounters.length / PAGE_SIZE));
  const pageEncounters = encounters.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

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
