-- AlterTable
ALTER TABLE "Exam" ADD COLUMN     "isActive" BOOLEAN NOT NULL DEFAULT false;

-- AlterTable
ALTER TABLE "ExamSession" ADD COLUMN     "duration" INTEGER;
