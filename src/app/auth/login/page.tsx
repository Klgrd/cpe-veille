import { AuthForm } from '@/components/auth/AuthForm';

export default function LoginPage() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <AuthForm view="login" />
    </div>
  );
}
