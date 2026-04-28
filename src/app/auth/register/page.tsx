import { AuthForm } from '@/components/auth/AuthForm';

export default function RegisterPage() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <AuthForm view="register" />
    </div>
  );
}
