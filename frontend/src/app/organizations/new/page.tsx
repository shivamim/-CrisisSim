import { OrganizationForm } from '@/components/OrganizationForm';

export default function NewOrganizationPage() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Create Organization</h1>
        <p className="text-gray-500">
          Set up your company profile to start running crisis simulations.
        </p>
      </div>
      <div className="bg-white rounded-xl shadow-sm border p-8">
        <OrganizationForm />
      </div>
    </div>
  );
}
