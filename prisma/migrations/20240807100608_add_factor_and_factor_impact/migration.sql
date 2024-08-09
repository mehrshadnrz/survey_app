-- CreateTable
CREATE TABLE "Factor" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "surveyId" INTEGER NOT NULL,

    CONSTRAINT "Factor_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "FactorImpact" (
    "id" SERIAL NOT NULL,
    "factorId" INTEGER NOT NULL,
    "optionId" INTEGER NOT NULL,
    "impact" INTEGER NOT NULL,
    "plus" BOOLEAN NOT NULL,

    CONSTRAINT "FactorImpact_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Factor" ADD CONSTRAINT "Factor_surveyId_fkey" FOREIGN KEY ("surveyId") REFERENCES "Survey"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "FactorImpact" ADD CONSTRAINT "FactorImpact_factorId_fkey" FOREIGN KEY ("factorId") REFERENCES "Factor"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "FactorImpact" ADD CONSTRAINT "FactorImpact_optionId_fkey" FOREIGN KEY ("optionId") REFERENCES "Option"("id") ON DELETE CASCADE ON UPDATE CASCADE;
