import type { Encounter } from '../assets/types';
import PatientRow from './PatientRow';

interface PatientTableProps {
  encounters: Encounter[];
}

export default function PatientTable({ encounters }: PatientTableProps) {
  return (
    <table className="min-w-full border-collapse border border-gray-200">
      <thead>
        <tr>
          <th className="border border-gray-200 p-2">Encounter ID</th>
          <th className="border border-gray-200 p-2">Patient Number</th>
          <th className="border border-gray-200 p-2">Age</th>
          <th className="border border-gray-200 p-2">Risk Level</th>
        </tr>
      </thead>
      <tbody>
        {encounters.map((encounter) => (
          <PatientRow key={encounter.encounter_id} encounter={encounter} />
        ))}
      </tbody>
    </table>
  );
}